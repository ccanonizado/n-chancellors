#include <stdio.h>
#include <stdlib.h>
#define N 4
#define TRUE 1
#define FALSE 0

int isSafe(int nopts[N+2], int row, int col, int last) {
  int i;

  printf("row: %d | col: %d | last: %d\n", row, col, last);

  // if filled before - safe but not allowed
  if (last == col) {
    printf("ALREADY MARKED AS CHANCELLOR\n");
    return FALSE;
  }

  // i is the current row - nopts[i] is the current col
  for(i=1; i<N+1; i++) {
    printf("i: %d | nopts[i]: %d\n", i, nopts[i]);
    // rook movement:
    if (nopts[i] != 0 && (row == i || col == nopts[i])) {
      printf("ROOK MOVEMENT\n");
      return FALSE;                  
    }
    // horse movements:

    /*
      0 1
      0 0
      x 0
    */
    if (nopts[i] != 0 && (i+2 == row && nopts[i]-1 == col)) {
      printf("KNIGHT MOVEMENT\n");
      return FALSE;
    }

    /*
      0 0 1
      x 0 0
    */
    else if (nopts[i] != 0 && (i+1 == row && nopts[i]-2 == col)) {
      printf("KNIGHT MOVEMENT\n");
      return FALSE;
    }

    /*
      1 0 0
      0 0 x
    */
    else if (nopts[i] != 0 && (i+1 == row && nopts[i]+2 == col)) {
      printf("KNIGHT MOVEMENT\n");
      return FALSE;
    }

    /*
      1 0
      0 0
      0 x
    */
    else if (nopts[i] != 0 && (i+2 == row && nopts[i]+1 == col)) {
      printf("KNIGHT MOVEMENT\n");
      return FALSE;
    }

  }
  
  // if all else fails and position is blank - safe
  if (nopts[row] == 0) {
    printf("SAFE FOR CHANCELLOR\n");
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

      else {
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
        if(last == -1){
          nopts[move] = 1;
          option[move][nopts[move]] = 1;
        }
        else{
          nopts[move] = last + 1;
          option[move][nopts[move]] = 1;
          last = -1;
          printf("move: %d | nopts[move]: %d\n", move, nopts[move]);
        }
      }

      // fill other slots of chancellors
      else {
        if(last == -1) i = 1;
        else i = last;
        for (i; i<N+1; i++) {
          printf("\n");
          printBoard(option);
          printf("\n");
          if (isSafe(nopts, move, i, last)) {
            option[move][i] = 1; // mark as chancellor
            nopts[move] = i; // store index of stack
            last = -1;
            printf("\n");
            printBoard(option);
            printf("\n");
            break;
          }
        }

        if (i == N+1) {
          nopts[move] = 0;
          move --;
          option[move][nopts[move]] = 0; // clear chancellor
          last = nopts[move];
          if(last == N){
            printf("Last: %d | i: %d | move: %d\n", last, i, move);
            nopts[move] = 0;
            move--;
            if(move == 0) nopts[move] = 0;
            else {
              option[move][nopts[move]] = 0; // clear chancellor
              last = nopts[move];
            }
          }
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