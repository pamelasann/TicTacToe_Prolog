:- dynamic matriz_actual/1.

% Initialize the matrix
inicializar_matriz :-
    retractall(matriz_actual(_)),
    assert(matriz_actual([[-, -, -], [-, -, -], [-, -, -]])).

% Modify an element in the matrix
modificar_matriz([Fila|RestoFilas], 1, C, NuevoElem, [NuevaFila|RestoFilas]) :-
    modificar_fila(Fila, C, NuevoElem, NuevaFila).
modificar_matriz([Fila|RestoFilas], F, C, NuevoElem, [Fila|NuevaMatriz]) :-
    F > 1,
    F1 is F - 1,
    modificar_matriz(RestoFilas, F1, C, NuevoElem, NuevaMatriz).

% Modify an element in a row
modificar_fila([_|RestoCols], 1, NuevoElem, [NuevoElem|RestoCols]).
modificar_fila([Col|RestoCols], C, NuevoElem, [Col|NuevaFila]) :-
    C > 1,
    C1 is C - 1,
    modificar_fila(RestoCols, C1, NuevoElem, NuevaFila).

% Modify the globally stored matrix
modificar_matriz_global(F, C, NuevoElem) :-
    matriz_actual(Matriz),
    modificar_matriz(Matriz, F, C, NuevoElem, NuevaMatriz),
    retractall(matriz_actual(_)),
    assert(matriz_actual(NuevaMatriz)).

% Display the current matrix
mostrar_matriz :-
    matriz_actual(Matriz),
    convert_to_string(Matriz, StringMatriz),
    write(StringMatriz), nl.

convert_to_string([], []).
convert_to_string([H|T], [HString|TString]) :-
    convert_row_to_string(H, HString),
    convert_to_string(T, TString).

convert_row_to_string([], []).
convert_row_to_string([H|T], [HString|TString]) :-
    (H = '-' -> HString = "\"-\""
    ; H = 'x' -> HString = "\"x\""
    ; H = 'o' -> HString = "\"o\""
    ),
    convert_row_to_string(T, TString).

% Winning condition
gane :-
    matriz_actual(Matriz),
    (   fila_ganadora(Matriz, X)
    ;   columna_ganadora(Matriz, X)
    ;   diagonal_ganadora(Matriz, X)
    ),
    !,
    (X \= '-' -> write('El ganador es: '), write(X), nl ; true).

% Check winning rows
fila_ganadora([[X,X,X], _, _], X) :- X \= '-'.
fila_ganadora([_, [X,X,X], _], X) :- X \= '-'.
fila_ganadora([_, _, [X,X,X]], X) :- X \= '-'.

% Check winning columns
columna_ganadora([[X,_,_], [X,_,_], [X,_,_]], X) :- X \= '-'.
columna_ganadora([[_,X,_], [_,X,_], [_,X,_]], X) :- X \= '-'.
columna_ganadora([[_,_,X], [_,_,X], [_,_,X]], X) :- X \= '-'.

% Check winning diagonals
diagonal_ganadora([[X,_,_], [_,X,_], [_,_,X]], X) :- X \= '-'.
diagonal_ganadora([[_,_,X], [_,X,_], [X,_,_]], X) :- X \= '-'.

% Draw condition
empate :-
    matriz_actual(Matriz),
    flatten(Matriz, Lista),
    \+ member('-', Lista),
    \+ gane,
    (forall(member(E, Lista), (E = 'x' ; E = 'o')) ->
        write('El juego es un empate'), nl
    ; true).

% Modify move to check win/draw
jugada(Jugador, Fila, Columna) :-
    modificar_matriz_global(Fila, Columna, Jugador),
    mostrar_matriz,
    (   gane
    ;   empate
    ;   Jugador = 'x' -> computer_move
    ).

% Generate a random move
random_move(Fila, Columna) :-
    findall((F,C), (between(1, 3, F), between(1, 3, C), matriz_actual(M), nth1(F, M, Row), nth1(C, Row, '-')), Moves),
    random_member((Fila, Columna), Moves).

% Computer move logic
computer_move :-
    matriz_actual(Matriz),
    (   find_winning_move('o', Matriz, F, C)
    ->  modificar_matriz_global(F, C, 'o'), mostrar_matriz, (gane ; empate)
    ;   find_winning_move('x', Matriz, F, C)
    ->  modificar_matriz_global(F, C, 'o'), mostrar_matriz, (gane ; empate)
    ;   random_move(F, C)
    ->  modificar_matriz_global(F, C, 'o'), mostrar_matriz, (gane ; empate)
    ).

% Find a potential winning or blocking move
find_winning_move(Player, Matriz, F, C) :-
    between(1, 3, F),
    between(1, 3, C),
    nth1(F, Matriz, Row),
    nth1(C, Row, '-'),
    modificar_matriz(Matriz, F, C, Player, NuevoMatriz),
    (fila_ganadora(NuevoMatriz, Player)
    ; columna_ganadora(NuevoMatriz, Player)
    ; diagonal_ganadora(NuevoMatriz, Player)).

% Start the game
iniciar_juego :-
    inicializar_matriz,
    mostrar_matriz.