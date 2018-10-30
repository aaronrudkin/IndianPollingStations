library(leaflet) # Plot map
library(mapview) # Save map

# Load full results
polling = read.csv("../out.csv")

# Sample 300 stations to plot
polling2  = polling[sample(1:nrow(polling), 300, replace=FALSE), ]

# Custom icon to make map pins smaller
smallIcon = makeIcon(
    iconUrl = "pin.png",
    iconWidth = 12, iconHeight = 12
)

# Plot map
map = leaflet(polling2) %>% addProviderTiles(providers$CartoDB.Positron) %>% 
    setView(lng=78, lat=22, zoom=5) %>%
    addMarkers(icon=smallIcon)
map

# Save map
mapshot(map, file = "map.png")