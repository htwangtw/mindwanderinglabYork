#load data
data<-read.csv('CS_SCCA_Paper.csv', sep=',', header = TRUE)

#load ggplot 2
require(ggplot2)

#assign the plot to a variable
p2<- (
  # scatter plot main data
  # the data need to be in dataframe format. x and y can refer directly to the variables
  ggplot(data, aes(x=SCCA_BOOTS_6_Mean, y=FAC1_QD_Rotation)) 
  # dot size, color and shape etc.
  + geom_point(shape=19, size = 2, colour="grey50") 
  # 95% confidence interval and regression line
  + geom_smooth(method=lm, colour="black", size = 1, fullrange = TRUE)
  # title and axis lable
  + ggtitle("Canonical Component 3")
  + ylab("Principle component score: poor Well -being") 
  + xlab("Canonical Component Score")
  # limits of the axises
  + xlim(-5, 5) + ylim(-5, 5)
  
) 

# display the plot, this is the default look
p2

# add APA format theme
p2 + theme_classic() +theme(
  axis.line.x = element_line(colour = "black"),
  axis.line.y = element_line(colour = "black")
  )

#save the plot
ggsave("scatter3-wb.png", width = 4.5, height = 4)
