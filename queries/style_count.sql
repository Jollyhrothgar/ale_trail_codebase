SELECT breweries.style_name,count(distinct breweries.beer_name) as number_of_beers FROM breweries GROUP BY breweries.style_name ORDER BY number_of_beers desc; 
