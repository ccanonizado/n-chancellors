#include <stdio.h>
#include <stdlib.h>
#define N 4

void printBoard(int board[N+2][N+2]) {
  int i, j;
  for(i=1; i<N+1; i++) {
    for(j=1; j<N+1; j++) {
      printf("%d ", board[i][j]);
    }
    printf("\n");
  }
}

int main() {
  int i, move, start, solutions;
  int nopts[N+2]; // array of top of stacks
  int option[N+2][N+2] = {}; // array of stacks of options

  move = start = solutions = 0;
  nopts[start] = 1;

  // while dummy stack is not empty
  // while(nopts[start] > 0) {

  // }

  printf("Blank %dx%d solutions: %d\n", N, N, solutions);
  return 0;
}