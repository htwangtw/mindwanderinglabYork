library(readxl)

data<-read_excel('scatterplot.xlsx')
attach(data)

#Brain 1
plot(UUT_total,SCCA_LOSO_Brain_1,  main="UUT x LOSO_RS_1", 
     xlab="UUT_N", ylab="SCCA_RS_LOSO_1", pch=19)
abline(lm(SCCA_LOSO_Brain_1~UUT_total), col="red") # regression line (y~x) 

plot(RAPM_PROP_ACC_36,SCCA_LOSO_Brain_1,  main="RAPM x LOSO_RS_1", 
     xlab="RAPM_N", ylab="SCCA_RS_LOSO_1", pch=19)
abline(lm(SCCA_LOSO_Brain_1~RAPM_PROP_ACC_36), col="red") # regression line (y~x)

#Task 1
SWITCH_EFF <- -1 *SWITCHCOST
plot(SWITCH_EFF,SCCA_LOSO_MWQ_1,  main="SWITCHCOST x LOSO_MWQ_1", 
     xlab="SWITCHCOST", ylab="SCCA_MWQ_LOSO_1", pch=19)
abline(lm(SCCA_LOSO_MWQ_1~SWITCH_EFF), col="red") # regression line (y~x)

plot(`RJT_PW_EFF_STRONG `,SCCA_LOSO_MWQ_1,  main="RJT_PW_EFF_STRONG x LOSO_MWQ_1", 
     xlab="RJT_PW_EFF_STRONG", ylab="SCCA_MWQ_LOSO_1", pch=19)
abline(lm(SCCA_LOSO_MWQ_1~`RJT_PW_EFF_STRONG `), col="red") # regression line (y~x)

plot(VFT_CAT,SCCA_LOSO_MWQ_1,  main="VFT_CAT x LOSO_MWQ_1", 
     xlab="VFT_CAT", ylab="SCCA_MWQ_LOSO_1", pch=19)
abline(lm(SCCA_LOSO_MWQ_1~VFT_CAT), col="red") # regression line (y~x)

#Brain2
plot(UUT_total,SCCA_LOSO_Brain_2,  main="UUT x LOSO_RS_2", 
     xlab="UUT_N", ylab="SCCA_RS_LOSO_2", pch=19)
abline(lm(SCCA_LOSO_Brain_2~UUT_total), col="red") # regression line (y~x) 

#Task 2
plot(MT_ACC,SCCA_LOSO_MWQ_2,  main="MT x LOSO_RS_2", 
     xlab="MT_ACC", ylab="SCCA_RS_LOSO_2", pch=19)
abline(lm(SCCA_LOSO_MWQ_2~MT_ACC), col="red") # regression line (y~x) 

plot(UUT_total,SCCA_LOSO_MWQ_2,  main="UUT x LOSO_MWQ_2", 
     xlab="UUT_N", ylab="SCCA_RS_MWQ_2", pch=19)
abline(lm(SCCA_LOSO_MWQ_2~UUT_total), col="red") # regression line (y~x) 

#Task3

plot(MT_ACC,SCCA_LOSO_MWQ_3,  main="MT x LOSO_MWQ_3", 
     xlab="MT_ACC", ylab="SCCA_MWQ_LOSO_3", pch=19)
abline(lm(SCCA_LOSO_MWQ_3~MT_ACC), col="red") # regression line (y~x) 

plot(`RJT_PW_EFF_STRONG `,SCCA_LOSO_MWQ_3,  main="RJT_PW_EFF_STRONG x LOSO_MWQ_3", 
     xlab="RJT_PW_EFF_STRONG", ylab="SCCA_MWQ_LOSO_3", pch=19)
abline(lm(SCCA_LOSO_MWQ_3~`RJT_PW_EFF_STRONG `), col="red") # regression line (y~x)

#Task 4
plot(`RJT_PW_EFF_STRONG `,SCCA_LOSO_MWQ_4,  main="RJT_PW_EFF_STRONG x LOSO_MWQ_4", 
     xlab="RJT_PW_EFF_STRONG", ylab="SCCA_MWQ_LOSO_4", pch=19)
abline(lm(SCCA_LOSO_MWQ_4~`RJT_PW_EFF_STRONG `), col="red") # regression line (y~x)

plot(SWITCH_EFF,SCCA_LOSO_MWQ_4,  main="SWITCH_EFF x LOSO_MWQ_4", 
     xlab="SWITCH_EFF", ylab="SCCA_MWQ_LOSO_4", pch=19)
abline(lm(SCCA_LOSO_MWQ_4~SWITCH_EFF), col="red") # regression line (y~x)







