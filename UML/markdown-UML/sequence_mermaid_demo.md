```mermaid
%% Example of sequence diagram
sequenceDiagram
Title: Here is a title
    participant A as Alice
    participant B as Bob
    participant C
    participant D

    A->+B: Normal line 
    B-->C: Dashed line 
    C->>D: Open arrow 
    D-->>-A: Dashed open arrow
       
	loop Daily query
        A->>B: Hello Bob, how are you?
        alt is sick
            B->>A: Not so good :(
        else is well
            B->>A: Feeling fresh like a daisy
        end
        opt Extra response
            D->>C: Thanks for asking
        end
    end
    
    Note left of A: Note to the\n left of A 
	Note right of A: Note to the\n right of A 
	Note over C,D: Note over both C and D
	Note over A: Note over A 
```






