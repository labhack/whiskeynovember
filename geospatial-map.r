#install.packages("devtools")
library("devtools")
#devtools::install_github("R-api","plotly")
library(plotly)
library(maps)
library(ggmap)

p <- plotly(username="cimmone", key="xxo5pzyvwi") 

data = read.csv("C:/jammers.csv", header=TRUE)

trace1 <- list(x=map("state")$x,
               y=map("state")$y)
trace2 <- list(x= data$lon,
               y=data$lat,
               type="scatter",
               mode="markers",
               marker=list(
                 "size"=data$intensity,
                 "opacity"=0.5)
)
response <- p$plotly(trace1,trace2)
url <- response$url
filename <- response$filename
browseURL(response$url)