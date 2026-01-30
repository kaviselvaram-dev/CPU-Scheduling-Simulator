#include<stdio.h>
int main(){
 int b[10],p[10],nb,np,i,j,alloc[10],ch;
 printf("Blocks: "); scanf("%d",&nb);
 printf("Processes: "); scanf("%d",&np);
 printf("Block sizes: "); for(i=0;i<nb;i++) scanf("%d",&b[i]);
 printf("Process sizes: "); for(i=0;i<np;i++) scanf("%d",&p[i]);
 printf("1.First Fit 2.Best Fit 3.Worst Fit: "); scanf("%d",&ch);

 for(i=0;i<np;i++) alloc[i]=-1;

 for(i=0;i<np;i++){
  int best=-1;
  for(j=0;j<nb;j++){
   if(b[j]>=p[i]){
    if(ch==1){best=j;break;}                // First Fit
    if(ch==2 && (best==-1 || b[j]<b[best])) best=j; // Best Fit
    if(ch==3 && (best==-1 || b[j]>b[best])) best=j; // Worst Fit
   }
  }
  if(best!=-1){alloc[i]=best; b[best]-=p[i];}
 }

 printf("\nProcess\tSize\tBlock\n");
 for(i=0;i<np;i++){
  if(alloc[i]!=-1) printf("P%d\t%d\tB%d\n",i+1,p[i],alloc[i]+1);
  else printf("P%d\t%d\tNot Allocated\n",i+1,p[i]);
 }
}