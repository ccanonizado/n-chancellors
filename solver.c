#include <stdio.h>
#include <stdlib.h>
#define TRUE 1
#define FALSE 0

int isSafe(int ** option, int * nopts, int row, int col, int last, int N) {
  int i;

  // if initial chancellor - safe but check usage below
  if(option[row][col] == 2) {
    return TRUE;
  }

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
      1 0
      0 0
      0 x
    */
    else if(nopts[i] != 0 && (i+2 == row && nopts[i]+1 == col)) {
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
      x 0 0
      0 0 1
    */
    else if(nopts[i] != 0 && (i-1 == row && nopts[i]-2 == col)) {
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
      0 0 x
      1 0 0
    */
    else if(nopts[i] != 0 && (i-1 == row && nopts[i]+2 == col)) {
      return FALSE;
    }

    /*
      x 0
      0 0
      0 1
    */
    else if(nopts[i] != 0 && (i-2 == row && nopts[i]-1 == col)) {
      return FALSE;
    }

    /*
      0 x
      0 0
      1 0
    */
    else if(nopts[i] != 0 && (i-2 == row && nopts[i]+1 == col)) {
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
  int N, i, j, k, boards, start, move, last, solutions;
  FILE * fp;

  fp = fopen("input4.txt", "r");
  fscanf(fp, "%d", &boards);
  
  // loop program depending on number of puzzles
  for(k=0; k<boards; k++) {

    printf("\nSolving Board %d:\n", k+1);
    
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
          if(isSafe(option, nopts, i, j, 0, N)) {
            option[i][j] = 2; // mark as 2 (never remove)
            nopts[i] = j;  // store top of stack
          }
          else {
            // initial chancellor placed is invalid
            printf("NO SOLUTION!\n");
            return 0;
          }
        }
      }
    }

    start = 0;

    // find start if there are initial chancellors
    for(i=1; i<N+1; i++) {
      for(j=1; j<N+1; j++) {
        if(option[i][j] == 2) {
          start = i;
        }
      }

      if(start != i) {
        break;
      }
    }

    // initialize variables
    last = -1;
    move = start;
    solutions = 0;
    if(start == 0) {
      nopts[start] = 1;
    }

    // while dummy stack is not empty
    while(nopts[start] > 0) {

      if(nopts[move] > 0) {

        if(last == -1) {
          move++;

          // put zero if NO initial chancellor
          if(option[move][nopts[move]] != 2) {
            nopts[move] = 0;
          }
        }

        else {

          // put zero if NO initial chancellor
          if(option[move][nopts[move]] != 2) {
            nopts[move] = 0;
          }
        }
        
        // solution found
        if(move == N+1) {
          solutions++;
          printf("Solution found!\n");
          printBoard(option, N);
          printf("\n");
        }

        // first chancellor if no initial exists
        else if(move == 1) {
          for(i = last == -1 ? 1 : last; i<N+1; i++) {
            // check every column of first row
            if(isSafe(option, nopts, move, i, last, N)) {
              option[move][i] = 1; // mark as chancellor
              nopts[move] = i; // store index of stack
              last = -1;
            }
          }
        }

        // fill other slots of chancellors
        else {
          for(i = last == -1 ? 1 : last; i<N+1; i++) {
            // check every column of current row
            if(isSafe(option, nopts, move, i, last, N)) {
              // only add new chancellor if no initial exists
              if(option[move][i] != 2) {
                option[move][i] = 1; // mark as chancellor
                nopts[move] = i; // store index of stack
                last = -1;
              }
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
              if(move == start) nopts[move] = 0;
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
        if(option[move][nopts[move]] != 2) {
          option[move][nopts[move]] = 0; // clear chancellor
          last = nopts[move];
        }
      }
    }

    if (solutions != 0) {
      printf("Board %d Solutions: %d\n", k+1, solutions);
    }

    else {
      printf("NO SOLUTIONS!\n");
    }

  }
  fclose(fp);
  

  return 0;
}