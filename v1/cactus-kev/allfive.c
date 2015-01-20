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

#define ITERATIONS 1000

main()
{
    int deck[52], hand[5], shuffle[52];
    int a, b, c, d, e, i, j;

    // seed the random number generator
    srand48( getpid() );

    // initialize the deck
    init_deck( deck );
    init_deck( shuffle );

    // loop over every possible five-card hand
    for(a=0;a<48;a++) {
        hand[0] = deck[a];

        for(b=a+1;b<49;b++) {
            hand[1] = deck[b];

            for(c=b+1;c<50;c++) {
                hand[2] = deck[c];

                // Iterate over hero hands
                for(d=c+1;d<51;d++) {

                    for(e=d+1;e<52;e++) {
                        for (i = 0; i < 52; i++) {
                            if (deck[e] == shuffle[i]) {
                                int temp = shuffle[51];
                                shuffle[51] = shuffle[i];
                                shuffle[i] = temp;
                                break;
                            }
                        }
                        for (i = 0; i < 52; i++) {
                            if (deck[d] == shuffle[i]) {
                                int temp = shuffle[50];
                                shuffle[50] = shuffle[i];
                                shuffle[i] = temp;
                                break;
                            }
                        }
                        for (i = 0; i < 52; i++) {
                            if (deck[c] == shuffle[i]) {
                                int temp = shuffle[49];
                                shuffle[49] = shuffle[i];
                                shuffle[i] = temp;
                                break;
                            }
                        }
                        for (i = 0; i < 52; i++) {
                            if (deck[b] == shuffle[i]) {
                                int temp = shuffle[48];
                                shuffle[48] = shuffle[i];
                                shuffle[i] = temp;
                                break;
                            }
                        }
                        for (i = 0; i < 52; i++) {
                            if (deck[a] == shuffle[i]) {
                                int temp = shuffle[47];
                                shuffle[47] = shuffle[i];
                                shuffle[i] = temp;
                                break;
                            }
                        }
                        double win_count = 0.0;
                        for (i = 0; i < ITERATIONS; i++) {
                            for (j = 0; j < 4; j++) {
                                int r = rand() % (47-j);
                                int temp = shuffle[r];
                                shuffle[r] = shuffle[46-j];
                                shuffle[46-j] = temp;
                            }
                            hand[3] = deck[d];
                            hand[4] = deck[e];

                            // turn and river
                            hand[5] = shuffle[43];
                            hand[6] = shuffle[44];
                            short our_score = eval_7hand(hand);

                            // change hand to opponent hand
                            hand[3] = shuffle[45];
                            hand[4] = shuffle[46];
                            short their_score = eval_7hand(hand);

                            // score calculation
                            if (our_score < their_score)
                                win_count+=1.0;
                            else if (our_score == their_score)
                                win_count+=0.5;
                        }
                        printf("%.3f ", win_count / ITERATIONS);
                    }
                }
                printf("\n");
            }
        }
    }

}
