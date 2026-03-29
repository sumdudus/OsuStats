# OsuStats
A simple TUI app for displaying your ( or somebody else's ) Osu! game stats.

## Previews
<img width="917" height="328" alt="image" src="https://github.com/user-attachments/assets/97be2ca5-2df5-45b2-b2f9-adba42e62cc9" />
<img width="785" height="347" alt="image" src="https://github.com/user-attachments/assets/16f118a7-8b04-4813-a83e-e2ca5ed3c484" />

## How to use
1. Clone the repository:  
  ```git clone https://github.com/sumdudus/OsuStats```  
2. Navigate to the new Local Directory and create a virtual enviorment:  
  ```cd OsuStats```  
  ```python -m venv venv```  
3. Activate the virtual enviorment and install dependencies:  
  ```source venv/bin/activate```  
  ```pip install ossapi typing_utils```  
4. Run the file and go through setup process:  
  ```python osuStats.py```

## Notes
Currently, if you wish to change your settings you have to manually edit them in the [.config file](osuStats/OsuStats.config).
The script only works on linux so far due to MacOS encountering issues with the ossapi library and Windows not being always being able to read ANSI color codes.

## Future Plans:
- [ ] Complete setup script:  
  - [ ] ├ Add error checks  
  - [ ] └ Icon options:  
    - [ ] ├ Display client icon / regular osu icon  
    - [ ] ├ Display user profile picture
    - [ ] └ Better Osu!Lazer and Stable icons
  - [ ] ├ Color options  
  - [ ] ├ Different formats / pipes  
  - [ ] └ Add a way to change config options from within the terminal  
- [ ] Optimize and Clean up code  
