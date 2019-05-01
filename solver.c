#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0

int isSafe(int * nopts, int row, int col, int last, int N) {
  int i;

  // if filled before - safe but not allowed
  if(last == col) {
    return FALSE;
  }

  // i is the current row - nopts[i] is the current col
  for(i=1; i<N+1; i++) {

    // rook movement:
    if(nopts[i] != 0 && (row == i || col == nopts[i])) {
      return FALSE;                  
    }

    // horse movements:

    /*
      0 1
      0 0
      x 0
    */
    if(nopts[i] != 0 && (i+2 == row && nopts[i]-1 == col)) {
      return FALSE;
    }

    /*
      0 0 1
      x 0 0
    */
    else if(nopts[i] != 0 && (i+1 == row && nopts[i]-2 == col)) {
      return FALSE;
    }

    /*
      1 0 0
      0 0 x
    */
    else if(nopts[i] != 0 && (i+1 == row && nopts[i]+2 == col)) {
      return FALSE;
    }

    /*
      1 0
      0 0
      0 x
    */
    else if(nopts[i] != 0 && (i+2 == row && nopts[i]+1 == col)) {
      return FALSE;
    }

  }
  
  // if all else fails and position is blank - safe
  if(nopts[row] == 0) {
    return TRUE;
  }

  // the position is safe
  return TRUE;
}

// 1/2 for chancellor - 0 for blank
void printBoard(int ** option, int N) {
  int i, j;

  for(i=1; i<N+1; i++) {
    for(j=1; j<N+1; j++) {
      printf(option[i][j] == 1 || option[i][j] == 2 ? "C " : "0 ");
    }
    printf("\n");
  }
}

int main() {
  int N, i, j, k, puzzles, start, move, last, solutions;
  FILE * fp;

  fp = fopen("input.txt", "r");
  fscanf(fp, "%d", &puzzles);
  
  // loop program depending on number of puzzles
  for(k=0; k<puzzles; k++) {
    
    fscanf(fp, "%d", &N);
    int * nopts = (int *) malloc(sizeof(int) * (N+2)); // array of top of stacks
    int ** option = (int **) malloc(sizeof(int *) * (N+2)); // array of stacks of options

    // allocate memory for board and initialize nopts
    for(i=0; i<N+2; i++) {
      option[i] = (int *) malloc(sizeof(int) * (N+2));
      nopts[i] = 0;
    }

    // copy contents of initial board
    for(i=1; i<N+1; i++) {
      for(j=1; j<N+1; j++) {
        fscanf(fp, "%d", &option[i][j]);
        
        // if there is initial chancellor
        if(option[i][j] == 1) {
          option[i][j] = 2; // mark as 2 (never remove)
          nopts[i] = j;  // store top of stack
        }
      }
    }

    move = start = solutions = 0;
    nopts[start] = 1;
    last = -1;

    // while dummy stack is not empty
    while(nopts[start] > 0) {

      if(nopts[move] > 0) {

        // first step
        if(move == start) {
          move = 0;
        }

        if(last == -1) {
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
          printBoard(option, N);
          printf("\n");
        }

        // initial first chancellor
        else if(move == 1) {
          if(last == -1) {
            nopts[move] = 1;
            option[move][nopts[move]] = 1;
          }
          else {
            nopts[move] = last + 1;
            option[move][nopts[move]] = 1;
            last = -1;
          }
        }

        // fill other slots of chancellors
        else {
          if(last == -1) i = 1;
          else i = last;
          for(i; i<N+1; i++) {
            if(isSafe(nopts, move, i, last, N)) {
              option[move][i] = 1; // mark as chancellor
              nopts[move] = i; // store index of stack
              last = -1;
              break;
            }
          }

          // backtrack
          if(i == N+1) {
            nopts[move] = 0;
            move--;
            option[move][nopts[move]] = 0; // clear chancellor
            last = nopts[move];
            // ANOTHER BACKTRACK IF THE PREV MOVE EXHAUSTED ALL POSSIBLE CANDIDATES
            if(last == N) {
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
        move--;
        option[move][nopts[move]] = 0; // clear chancellor
        last = nopts[move];
      }
    }
    printf("Blank %dx%d solutions: %d\n", N, N, solutions);
  }

  fclose(fp);

  return 0;
}