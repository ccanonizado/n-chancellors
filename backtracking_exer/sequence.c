#include <stdio.h>
#include <stdlib.h>
#define N 3

int main(){
	int start, move;
	int nopts[N+2]; //array top of stacks
	int option[N+2][N+2]; //array stacks of options
	int i, candidate;

	move = start = 0; 
	nopts[start]= 1;
	
	while (nopts[start] >0)
	{
		if(nopts[move]>0)
		{
			move++;
			nopts[move]=0; //initialize new move

			//print - solution found!
			if(move==N+1){
				for(i=1;i<move;i++)
					printf("%2i",option[i][nopts[i]]);
				printf("\n");
			}
			//populate
			else //find candidates
			{
				for(candidate = N; candidate >=1; candidate --) 
				{
					nopts[move]++;
					option[move][nopts[move]] = candidate;
				} 
			}
		}
		else 
		{
			//backtrack
			move--;
			nopts[move]--;
		}
	}

}
