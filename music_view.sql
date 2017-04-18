create view music_view 
	as 
select 
	Album.name as albumName, 
	Album.releaseDate as albumReleaseDate, 
	Artist.name as artistName,  
	Artist.placeOfBith as artistPlaceOfBirth,
	Artist.dateOfBirth as artistDateOfBirth,
	Genres.name as genreName,
	Track.name as trackName
from Album 
join Track 
	on Track.albumID = Album.albumID
join Artist 
	on Artist.id = Album.artsitID 
join Genres 
	on Genres.id = Album.genreID