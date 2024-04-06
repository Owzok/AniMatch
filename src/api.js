export let filtered_ids = [], movie_ids = [], short_ids = [], long_ids = [], old_ids = [], newer_ids = [], imageExists, imageSrc;
export let title = "", episodes = "", members = "", score = "", ranked = "", desc = "", genres = "", genresArray = [];

export async function movieFilter(fetched_data) {
    const response = await fetch('http://127.0.0.1:5000/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            min_episodes: 1,
            max_episodes: 1,
            fetched_data: fetched_data
        }),
    });

    if (response.ok) {
        const filteredData = await response.json();

        console.log('Filtered Data:', filteredData);
        movie_ids = filteredData; 

        await fetch('http://127.0.0.1:5000/profile_pics', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                ids: filteredData
            }),
        });
    } else {
        console.error('Failed to fetch data');
    }
}

export async function shortFilter(fetched_data){
    const response = await fetch('http://127.0.0.1:5000/filter', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        min_episodes: 6,
        max_episodes: 13,
        fetched_data: fetched_data
      }),
    });

    if (response.ok) {
      const filteredData = await response.json();

      console.log('Filtered Data:', filteredData);
      short_ids = filteredData;
      
      await fetch('http://127.0.0.1:5000/profile_pics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ids: filteredData
        }),
      });
    } else {
      console.error('Failed to fetch data');
    }
}

export async function longFilter(fetched_data){
    const response = await fetch('http://127.0.0.1:5000/filter', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        min_episodes: 50,
        fetched_data: fetched_data
      }),
    });

    if (response.ok) {
      const filteredData = await response.json();

      console.log('Filtered Data:', filteredData);
      long_ids = filteredData;
      
      await fetch('http://127.0.0.1:5000/profile_pics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ids: filteredData
        }),
      });
    } else {
      console.error('Failed to fetch data');
    }
}

export async function oldFilter(fetched_data){
    const response = await fetch('http://127.0.0.1:5000/filter', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        max_year: 2003,
        fetched_data: fetched_data
      }),
    });

    if (response.ok) {
      const filteredData = await response.json();

      console.log('Filtered Data:', filteredData);
      old_ids = filteredData;
      
      await fetch('http://127.0.0.1:5000/profile_pics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ids: filteredData
        }),
      });
    } else {
      console.error('Failed to fetch data');
    }
}

export async function newerFilter(fetched_data){
    const response = await fetch('http://127.0.0.1:5000/filter', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        min_year: 2018,
        fetched_data: fetched_data
      }),
    });

    if (response.ok) {
      const filteredData = await response.json();

      console.log('Filtered Data:', filteredData);
      newer_ids = filteredData;
      
      await fetch('http://127.0.0.1:5000/profile_pics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ids: filteredData
        }),
      });
    } else {
      console.error('Failed to fetch data');
    }
}

export async function applyFilters(fetched_data){
    const response = await fetch('http://127.0.0.1:5000/filter', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        min_score: from_val2,
        max_score: to_val2,
        min_episodes: from_val1,
        max_episodes: to_val1,
        min_year: from_val3,
        max_year: to_val3,
        fetched_data: fetched_data
      }),
    });

    if (response.ok) {
      const filteredData = await response.json();

      console.log('Filtered Data:', filteredData);
      filtered_ids = filteredData;
      
      await fetch('http://127.0.0.1:5000/profile_pics', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ids: filteredData
        }),
      });

      //sendToRecommendRoute(filteredData);
    } else {
      console.error('Failed to fetch data');
    }
}

export async function generateImage(current_id) {
    const api_url = 'http://127.0.0.1:5000/scrape_image';
  
    try {
      const response = await fetch(`/download/${current_id}.jpg`);
      imageExists = response.ok;
  
      if (imageExists) {
        imageSrc = `/download/${current_id}.jpg`;
      } else {
        const response = await fetch(api_url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ id: current_id }),
        });
  
        if (response.ok) {
          console.log("Answered!");
          const responseData = await response.json();
  
          if (responseData.success) {
            imageExists = true;
            imageSrc = `/download/${current_id}.jpg`;
            console.log(imageExists);
          } else {
            console.error('API request was not successful:', responseData.error);
          }
        } else {
          console.error('API request failed with status code:', response.status);
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
}

export async function updateInfo(current_id) {
  try {
    const response = await fetch('http://127.0.0.1:5000/get_info', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: current_id }),
    });

    if (response.ok) {
      const data = await response.json();
      console.log(data);
      title = data.Name;
      episodes = data.Episodes;
      if (episodes === '1'){
        episodes = 'Movie';
      }
      score = data.Score;
      members = data.Members;
      members = formatScore(data.Members);
      desc = data.synopsis;
      ranked = data.Ranked;
      genres = data.Genres;
      genresArray = genres.split(',').map(genre => genre.trim());
      console.log(genresArray);
    } else {
      console.error('Failed to fetch data');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}