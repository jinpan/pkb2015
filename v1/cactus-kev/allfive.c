#include <stdio.h>
#include "poker.h"

/*************************************************/
/*                                               */
/* This code tests my evaluator, by looping over */
/* all 2,598,960 possible five card hands, cal-  */
/* culating each hand's distinct value, and dis- */
/* playing the frequency count of each hand type */
/*                                               */
/* Kevin L. Suffecool, 2001                      */
/* suffecool@bigfoot.com                         */
/*                                               */
/*************************************************/

#define ITERATIONS 5000

main()
{
    int deck[52], hand[7], freq[10], shuffle[52];
    int a, b, c, i, j;

    // seed the random number generator
    srand48( getpid() );

    // initialize the deck
    init_deck( deck );
    init_deck( shuffle );

    // zero out the frequency array
    for ( i = 0; i < 10; i++ )
        freq[i] = 0;

    // loop over every possible two-card hand
    for(a=0;a<51;a++)
    {
        hand[0] = deck[a];
        for(b=a+1;b<52;b++)
        {
            for (c = 0; c < 52; c++) {
                if (deck[a] == shuffle[c]) {
                    int temp = shuffle[50];
                    shuffle[50] = shuffle[c];
                    shuffle[c] = temp;
                }
            }
            for (c = 0; c < 52; c++) {
                if (deck[b] == shuffle[c]) {
                    int temp = shuffle[51];
                    shuffle[51] = shuffle[c];
                    shuffle[c] = temp;
                }
            }
            double win_count = 0.0;
            for (i = 0; i < ITERATIONS; i++) {
                for (j = 0; j < 7; j++) {
                    int r;
                    while (shuffle[(r = rand() % (50-j))] == deck[a] 
                        || shuffle[r] == deck[b]);
                    if (r == 49-j) continue;
                    int temp = shuffle[r];
                    shuffle[r] = shuffle[49-j];
                    shuffle[49-j] = temp;
                }
                for (j = 0; j < 5; j++) {
                    hand[j] = shuffle[43+j];
                }
                hand[5] = shuffle[50];
                hand[6] = shuffle[51];
                short our_score = eval_7hand(hand); 
                hand[5] = shuffle[48];
                hand[6] = shuffle[49];
                short their_score = eval_7hand(hand);
                if (our_score < their_score)
                    win_count+=1.0;
                else if (our_score == their_score)
                    win_count+=0.0;
            }
            printf("Equity for %d %d is: %.5f\n", a, b, win_count / ITERATIONS);
        }
    }
}
