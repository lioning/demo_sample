#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/epoll.h>
#include <errno.h>

#define MAXEVENTS 64

static int
make_socket_non_blocking( int listenfd )
{
    int flags, s;

    flags = fcntl( listenfd, F_GETFL, 0 );

    if ( flags == -1 )
    {

        perror( "fcntl" );
        return(-1);
    }

    flags    |= O_NONBLOCK;

    s    = fcntl( listenfd, F_SETFL, flags );

    if ( s == -1 )
    {
        perror( "fcntl" );
        return(-1);
    }

    return(0);
}


static int
create_and_bind( char *port )
{

    struct addrinfo hints;

    struct addrinfo *result, *rp;
    int        s, listenfd;

    memset( &hints, 0, sizeof(struct addrinfo) );
    //hints.ai_family       = AF_UNSPEC;  /* Return IPv4 and IPv6 choices */
    hints.ai_family       = AF_INET;  /* Return IPv4 and IPv6 choices */
    hints.ai_socktype     = SOCK_STREAM;  /* We want a TCP socket */
    hints.ai_flags        = AI_PASSIVE;  /* All interfaces */

    s = getaddrinfo( NULL, port, &hints, &result );

    if ( s != 0 )
    {
        fprintf( stderr, "getaddrinfo: %s\n", gai_strerror( s ) );
        return(-1);
    }

    for ( rp = result; rp != NULL; rp = rp->ai_next )
    {
        listenfd = socket( rp->ai_family, rp->ai_socktype, rp->ai_protocol );

        if ( listenfd == -1 )
            continue;

        s = bind( listenfd, rp->ai_addr, rp->ai_addrlen );

        if ( s == 0 )
        {
            /* We managed to bind successfully! */
            break;
        }

        close( listenfd );
    }

    if ( rp == NULL )
    {
        fprintf( stderr, "Could not bind\n" );
        return(-1);
    }

    freeaddrinfo( result );

    return(listenfd);
}

static deal_accept_event(int efd, int listenfd)
{
    struct epoll_event    event;
    int    s =0;

    while ( 1 )
    {

        struct sockaddr in_addr;
        socklen_t       in_len;
        int        infd;
        char       hbuf[NI_MAXHOST], sbuf[NI_MAXSERV];

        in_len  = sizeof in_addr;
        infd    = accept( listenfd, &in_addr, &in_len );

        if ( infd == -1 )
        {
            /* We have processed all incoming
             * connections. */
            if ( (errno == EAGAIN) || (errno == EWOULDBLOCK) )
            {
                break;
            }
            /* error */
            else
            {
                perror( "accept" );
                break;
            }
        }

        s = getnameinfo( &in_addr, in_len,

                         hbuf, sizeof hbuf,
                         sbuf, sizeof sbuf,
                         NI_NUMERICHOST | NI_NUMERICSERV );

        if ( s == 0 )
        {
            printf( "Accepted connection on descriptor %d "
                    "(host=%s, port=%s)\n", infd, hbuf, sbuf );
        }


        /* Make the incoming socket non-blocking and add it to the
         * list of fds to monitor. */
        s = make_socket_non_blocking( infd );

        if ( s == -1 )
            abort();

        event.data.fd   = infd;
        event.events    = EPOLLIN | EPOLLET;

        s        = epoll_ctl( efd, EPOLL_CTL_ADD, infd, &event );
        if ( s == -1 )
        {
            perror( "epoll_ctl" );
            abort();
        }
    }
}

static deal_read_event(struct epoll_event    event)
{
    int need_to_close = 0;
    int    s =0;

    while ( 1 )
    {
        ssize_t count;
        char    buf[512];

        count = read( event.data.fd, buf, sizeof buf );

        if ( count == -1 )
        {
            /* If errno == EAGAIN, that means we have read all
             * data. So go back to the main loop. */
            if ( errno == EAGAIN )
            {
                break;
            }
            else
            {
                perror( "read" );
                need_to_close = 1;
                break;
            }
        }
        else if ( count == 0 )
        {
            /* End of file. The remote has closed the
             * connection. */
            need_to_close = 1;
            break;
        }

        /* Write the buffer to standard output */
        //s = write( 1, buf, count );

        s = write( event.data.fd, buf, count );

        if ( s == -1 )
        {
            perror( "write" );
            abort();
        }
        s = write( 1, buf, count);
        s = write( 1, "\n", sizeof("\n"));
    }

    if ( need_to_close )
    {
        printf( "Closed connection on descriptor %d\n",
                event.data.fd );

        /* Closing the descriptor will make epoll remove it
        *  from the set of descriptors which are monitored. */
        close( event.data.fd );
    }
}

int
main( int argc, char *argv[] )
{
    int            listenfd, s;
    int            efd;
    struct epoll_event    event;
    struct epoll_event    *events;

    if ( argc != 2 )
    {
        fprintf( stderr, "Usage: %s [port]\n", argv[0] );
        exit( EXIT_FAILURE );
    }

    listenfd = create_and_bind( argv[1] );
    if ( listenfd == -1 )
        abort();

    s = make_socket_non_blocking( listenfd );
    if ( s == -1 )
        abort();

    s = listen( listenfd, SOMAXCONN );
    if ( s == -1 )
    {
        perror( "listen" );
        abort();
    }

    efd = epoll_create1( 0 );
    if ( efd == -1 )
    {
        perror( "epoll_create" );
        abort();
    }

    event.data.fd   = listenfd;
    event.events    = EPOLLIN | EPOLLET;

    s        = epoll_ctl( efd, EPOLL_CTL_ADD, listenfd, &event );
    if ( s == -1 )
    {
        perror( "epoll_ctl" );
        abort();
    }

    /* Buffer where events are returned */
    events = calloc( MAXEVENTS, sizeof event );

    /* The event loop */
    while ( 1 )
    {
        int nfds, i;

        nfds = epoll_wait( efd, events, MAXEVENTS, -1 );

        if (nfds <= 0)
            continue;

        for ( i = 0; i < nfds; i++ )
        {
            /* We have a notification on the listening socket, which
                 * means one or more incoming connections. */
            if ( listenfd == events[i].data.fd )
            {
                deal_accept_event(efd, listenfd);
                continue;
                //while ( 1 )
                //{
                //
                //    struct sockaddr in_addr;
                //    socklen_t    in_len;
                //    int        infd;
                //    char        hbuf[NI_MAXHOST], sbuf[NI_MAXSERV];
                //
                //    in_len    = sizeof in_addr;
                //    infd    = accept( listenfd, &in_addr, &in_len );
                //
                //    if ( infd == -1 )
                //    {
                //        if ( (errno == EAGAIN) ||
                //                (errno == EWOULDBLOCK) )
                //        {
                //            /* We have processed all incoming
                //             * connections. */
                //            break;
                //        }
                //
                //        else
                //        {
                //            perror( "accept" );
                //            break;
                //        }
                //    }
                //
                //    s = getnameinfo( &in_addr, in_len,
                //
                //                     hbuf, sizeof hbuf,
                //                     sbuf, sizeof sbuf,
                //                     NI_NUMERICHOST | NI_NUMERICSERV );
                //
                //    if ( s == 0 )
                //    {
                //        printf( "Accepted connection on descriptor %d "
                //                "(host=%s, port=%s)\n", infd, hbuf, sbuf );
                //    }
                //
                //
                //    /* Make the incoming socket non-blocking and add it to the
                //     * list of fds to monitor. */
                //    s = make_socket_non_blocking( infd );
                //
                //    if ( s == -1 )
                //        abort();
                //
                //    event.data.fd    = infd;
                //
                //    event.events    = EPOLLIN | EPOLLET;
                //
                //    s        = epoll_ctl( efd, EPOLL_CTL_ADD, infd, &event );
                //
                //    if ( s == -1 )
                //    {
                //        perror( "epoll_ctl" );
                //        abort();
                //    }
                //}
            }

            /* We have data on the fd waiting to be read. Read and
                 * display it. We must read whatever data is available
                 * completely, as we are running in edge-triggered mode
                 * and won't get a notification again for the same
                 * data. */
            else if (events[i].events & EPOLLIN)
            {
                deal_read_event(events[i]);
                //int done = 0;
                //
                //while ( 1 )
                //{
                //    ssize_t count;
                //    char    buf[512];
                //
                //    count = read( events[i].data.fd, buf, sizeof buf );
                //
                //    if ( count == -1 )
                //    {
                //        /* If errno == EAGAIN, that means we have read all
                //         * data. So go back to the main loop. */
                //        if ( errno != EAGAIN )
                //        {
                //            perror( "read" );
                //            done = 1;
                //        }
                //        break;
                //    }
                //    else if ( count == 0 )
                //    {
                //        /* End of file. The remote has closed the
                //         * connection. */
                //        done = 1;
                //        break;
                //    }
                //
                //    /* Write the buffer to standard output */
                //    s = write( 1, buf, count );
                //
                //    if ( s == -1 )
                //    {
                //        perror( "write" );
                //        abort();
                //    }
                //}
                //
                //if ( done )
                //{
                //    printf( "Closed connection on descriptor %d\n",
                //            events[i].data.fd );
                //
                //    /* Closing the descriptor will make epoll remove it
                //    *  from the set of descriptors which are monitored. */
                //    close( events[i].data.fd );
                //}
            }
            else if (events[i].events & EPOLLOUT)
            {
                ;
            }
            /* An error has occured on this fd, or the socket is not
             * ready for reading (why were we notified then?) */
            else if ( (events[i].events & EPOLLERR) ||
                      (events[i].events & EPOLLHUP) ||
                      (!(events[i].events & EPOLLIN) ) )
            {
                fprintf( stderr, "epoll error\n" );
                close( events[i].data.fd );
                continue;
            }
        }
    }

    free( events );
    close( listenfd );

    return(EXIT_SUCCESS);
}
