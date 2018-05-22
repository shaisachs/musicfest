## MusicFest API

This site documents the creation of a static, [Schema.org](http://schema.org/)-integrated API for a music festival.

The project was inspired by [Porchfest](https://www.somervilleartscouncil.org/porchfest), an annual event in Somerville, MA in which musicians perform for free on porches throughout the city. Residents walk around from one venue to another, enjoying the music and getting to know their neighbors. It's a wonderful community event, and just one more thing that makes this city so special.

The code in this repository is a simple web scraper which converts the Porchfest home page into a JSON file, which is decorated in [JSON-LD](https://json-ld.org/) format to integrate with the relevant concepts from Schema.org - in particular [Event](http://schema.org/Event), [MusicGroup](http://schema.org/MusicGroup), and [Location](http://schema.org/Location). Due to some missing data points in the original data source, the API is not wholly compliant with Schema.org, but it's pretty close.

The resulting API is available at `GET https://shaisachs.github.io/musicfest/api.json`.

More details to come soon, on [my blog](https://shaisachs.github.io).