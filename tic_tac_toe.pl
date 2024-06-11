:- dynamic matriz_actual/1.

% Inicializar la matriz
inicializar_matriz :-
    retractall(matriz_actual(_)),  
    % Eliminar cualquier matriz almacenada previamente
    assert(matriz_actual([[-, -, -], [-, -, -], [-, -, -]])).

% Acceder a un elemento de la matriz ?
matriz(M, F, C, E) :-
    nth1(F, M, Fila),
    nth1(C, Fila, E).

% Modificar un elemento de la matriz
modificar_matriz([Fila|RestoFilas], 1, C, NuevoElem, [NuevaFila|RestoFilas]) :-
    modificar_fila(Fila, C, NuevoElem, NuevaFila).
modificar_matriz([Fila|RestoFilas], F, C, NuevoElem, [Fila|NuevaMatriz]) :-
    F > 1,
    F1 is F - 1,
    modificar_matriz(RestoFilas, F1, C, NuevoElem, NuevaMatriz).

% Modificar un elemento en una fila
modificar_fila([_|RestoCols], 1, NuevoElem, [NuevoElem|RestoCols]).
modificar_fila([Col|RestoCols], C, NuevoElem, [Col|NuevaFila]) :-
    C > 1,
    C1 is C - 1,
    modificar_fila(RestoCols, C1, NuevoElem, NuevaFila).

% Modificar la matriz almacenada globalmente
modificar_matriz_global(F, C, NuevoElem) :-
    matriz_actual(Matriz),
    modificar_matriz(Matriz, F, C, NuevoElem, NuevaMatriz),
    retractall(matriz_actual(_)),
    assert(matriz_actual(NuevaMatriz)).

% Mostrar la matriz actual
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


% Condición de gane
gane :-
    matriz_actual(Matriz),
    (   fila_ganadora(Matriz, X)
    ;   columna_ganadora(Matriz, X)
    ;   diagonal_ganadora(Matriz, X)
    ),
    !,  % Cortar para evitar mas soluciones
    (X \= '-' -> write('El ganador es: '), write(X), nl ; true).

% Verificar filas ganadoras
fila_ganadora([[X,X,X], _, _], X) :- X \= '-'.
fila_ganadora([_, [X,X,X], _], X) :- X \= '-'.
fila_ganadora([_, _, [X,X,X]], X) :- X \= '-'.

% Verificar columnas ganadoras
columna_ganadora([[X,_,_], [X,_,_], [X,_,_]], X) :- X \= '-'.
columna_ganadora([[_,X,_], [_,X,_], [_,X,_]], X) :- X \= '-'.
columna_ganadora([[_,_,X], [_,_,X], [_,_,X]], X) :- X \= '-'.

% Verificar diagonales ganadoras
diagonal_ganadora([[X,_,_], [_,X,_], [_,_,X]], X) :- X \= '-'.
diagonal_ganadora([[_,_,X], [_,X,_], [X,_,_]], X) :- X \= '-'.

% Condición para el caso de empate (todas las casillas llenas sin ganador)
empate :-
    matriz_actual(Matriz),
    flatten(Matriz, Lista),
    \+ member('-', Lista),  % Verificar que no haya elementos vacíos
    \+ gane,  % Asegurarse de que no hay un ganador
    (forall(member(E, Lista), (E = 'x' ; E = 'o')) ->
        write('El juego es un empate'), nl
    ; true).

% Modificar jugada para verificar gane y empate
jugada(Jugador, Fila, Columna) :-
    modificar_matriz_global(Fila, Columna, Jugador),
    mostrar_matriz,
    (   gane
    ;   empate
    ).

% Inicializar el juego
iniciar_juego :-
    inicializar_matriz,
    mostrar_matriz.
