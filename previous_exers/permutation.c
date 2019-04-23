#include <stdio.h>
#include <stdlib.h>
#define N 3

int main(){
	int start, move;
	int nopts[N+2]; //array of top of stacks
	int option[N+2][N+2]; //array of stacks of options
	int i, candidate;

	move = start = 0; 
	nopts[start]= 1;
	
	while (nopts[start] >0) //while dummy stack is not empty
	{
		if(nopts[move]>0) 
		{
			move++;
			nopts[move]=0; //initialize new move

			if(move==N+1) //solution found!
			{
				for(i=1;i<move;i++)
					printf("%2i",option[i][nopts[i]]);
				printf("\n");
			}
			else if(move == 1){
				for(candidate = N; candidate >=1; candidate --) 
				{
					nopts[move]++;
					option[move][nopts[move]] = candidate;
					printf("nopts[move] %i candidate %i:\n", nopts[move], candidate);           
				}
			}
			else{
				for(candidate=N;candidate>=1;candidate--)
				{
					for(i=move-1;i>=1;i--)
						if(candidate==option[i][nopts[i]]) break;
					if(!(i>=1))
						option[move][++nopts[move]] = candidate;
				}
			}
		}
		else 
		{
			move--;
			nopts[move]--;

		}
	}
}
