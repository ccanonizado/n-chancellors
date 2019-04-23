#include <stdio.h>
#include <stdlib.h>
#define N 4
#define TRUE 1
#define FALSE 0

int isSafe(int nopts[N+2], int row, int col, int last) {
  int i;

  // i is the current row - nopts[i] is the current col
  for(i=1; i<N+1; i++) {

    // rook movement:
    if (nopts[i] != 0 && (row == i || col == nopts[i]))
      return FALSE;                  

    // horse movements:

    /*
      0 x
      0
      1
    */
    if (i-2 == row && nopts[i]+1 == col)
      return FALSE;
 
    /*
      0 0 x
      1
    */
    else if (i-1 == row && nopts[i]+2 == col)
      return FALSE;

    /*
      1 0 0
          x
    */
    else if (i+1 == row && nopts[i]+2 == col)
      return FALSE;

    /*
      1
      0
      0 x
    */
    else if (i+2 == row && nopts[i]+1 == col)
      return FALSE;

    // if filled before - safe but not allowed
    if (last == i){
      printf("Last: %d | i: %d\n", last, i);
      nopts[i] = 0;
      return FALSE;
    }
    // if all else fails and position is blank - safe
    else if (nopts[i] == 0)
      return TRUE;
  }

  // the position is safe
  return TRUE;
}

// 1 for chancellor - 0 for blank
void printBoard(int option[N+2][N+2]) {
  int i, j;
  for(i=1; i<N+1; i++) {
    for(j=1; j<N+1; j++) {
      printf("%d ", option[i][j]);
    }
    printf("\n");
  }
}

int main() {
  int i, move, last, start, solutions;
  int nopts[N+2] = {}; // array of top of stacks
  int option[N+2][N+2] = {}; // array of stacks of options

  move = start = solutions = 0;
  nopts[start] = 1;
  last = -1;

  // while dummy stack is not empty
  while(nopts[start] > 0) {

    if(nopts[move] > 0) {

      if (last == -1) {
        move++;
        nopts[move] = 0;
      }
      
      // solution found
      if(move == N+1) {
        solutions++;
        printf("Solution found!\n");
        printBoard(option);
      }

      // initial first chancellor
      else if (move == 1) {
        nopts[move] = 1;
        option[move][nopts[move]] = 1;
      }

      // fill other slots of chancellors
      else {
        for (i=1; i<N+1; i++) {
          if (isSafe(nopts, i, move, last)) {
            option[move][i] = 1; // mark as chancellor
            nopts[move] = i; // store index of stack
            break;
          }
        }

        if (i == N+1) {
          printf("Last: %d | i: %d | move: %d\n", last, i, move);
          nopts[move] = 0;
          move --;
          option[move][nopts[move]] = 0; // clear chancellor
          last = nopts[move];
        }

      }
    }

    // backtrack
    else {
      move --;
      option[move][nopts[move]] = 0; // clear chancellor
      last = nopts[move];
    }
  }

  printf("Blank %dx%d solutions: %d\n", N, N, solutions);
  return 0;
}