# Create some fake data, this is how your data should be arranged as
df <- data.frame(cond=rep(c("cond_1", "cond_2", "cond_3"), each=20),
                 bin=rep(seq(5),12),
                 freq=c(runif(60, min=0, max=20)))

#+++++++++++++++++++++++++
# Function to calculate the mean and the standard deviation
# for each group
#+++++++++++++++++++++++++
# data : a data frame
# varname : the name of a column containing the variable
#to be summariezed
# groupnames : vector of column names to be used as
# grouping variables

data_summary <- function(data, varname, groupnames){
  require(plyr)
  summary_func <- function(x, col){
    c(mean = mean(x[[col]], na.rm=TRUE),
      se = sd(x[[col]], na.rm=TRUE))/sqrt(length(x[[col]]))
  }
  data_sum<-ddply(data, groupnames, .fun=summary_func,
                  varname)
  data_sum <- rename(data_sum, c("mean" = varname))
  return(data_sum)
}

# Calculate the summary
# note: if you want to calculating the summary outside r, please arrage the data into this format
df_summary <- data_summary(df, varname="freq", groupnames=c("cond", "bin"))
# head(df_summary)

require("ggplot2")
# create the basic plot
# plot the axis and set color differently according to conditions. 
# If you want to change types of line: linetype=cond
p<- ggplot(df_summary, aes(x=bin, y=freq, group=cond, color=cond))+ 
  # plot error bars
  # 'position' is optional. Use position_dodge to move overlapped errorbars horizontally.
  geom_errorbar(aes(ymin=freq-se, ymax=freq+se), size=0.5, width=.2, position=position_dodge(0.05))+
  # draw a lines to link the dots, you can set the size and linetype(see ggplot manual)
  geom_line(size=1)+
  # plot means as dots, you can set the size and shape(see ggplot manual)
  geom_point(shape=19, size = 4)+
  #set lables
  labs(title="Your title here",x="Bin", y = "data")

#add theme. base size is the general font size.
p + 
  theme_classic(base_size = 12, base_family = "") +
  theme(axis.line.x = element_line(color = "black", size=1),
  axis.line.y = element_line(color = "black", size=1))+
  # check ggplot manual for more colour brewers
  scale_color_brewer(palette="Dark2")
