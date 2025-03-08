# Taiko
      Taiko for Luoluo and BU

# ToDoList
      Overlay


# Song 
      1 ESE:
            https://ese.tjadataba.se/ESE/ESE
    
      2 Switch:
            https://docs.google.com/spreadsheets/d/1kjrQCERIihmhQPYSOelu16bpeJ-HKneBj5-dkoc2wRs/edit#gid=0


# Pip
      python virsion 3.11.6

      pip install tensorflow
      pip install ffmpeg
      pip install os
      pip install opencv-python                       
      pip install soundfile
      pip install pydub                                      
      pip install tqdm                                          
      pip install librosa matplotlib numpy         
      pip install matplotlib==3.7.0                   
      pip install numpy==1.26.0                          


# v2 
      #every thing in test is no need when runing the entire program,so they won't be explen.

      1 select song:

            (to select song in Taiko-switch and make some thing to let training be more eazy)

            1 open-myself:
                  made opentja by myself but not finish

            2 opentja:
                  chatgpt origin selectsong.py

            3 selectsong:
                  sort the song which don't have odd hitting point and level at 6~7 

            4 sorting_folder:
                  select all level 6~7 from the roof folder and put them in level 6~7 folder    (v2/data/level 6~7)
            
            5 unzip:
                  to unzip all zip file which put in sub folder and all of them are in a big roof folder


      2 split_song:

            (to split the song to many piece)

            1 readdata:
                  extract_level_value(folder_path):out put array which write in tja file
                        ->[LEVEL,BPM,OFFSET,piece] (piece要切的張數)

            2 song_sec:
                  calculate time for each piece
                        ->list[time of per piece]

            3 splitv2:
                  cut song to many piece and use OggToJpg/Spectrogram to let every piece of song(.ogg) turn to jpg
                        ->v2/data/split_ogg
                        ->v2/data/zip_testing_data (use OggToJpg/Spectrogram to make)


      3 OggToJpg:

            (to change ogg to jpg by fft)

            1 Spectrogram: 
                  to change ogg to jpg by fft
                        ->v2/data/zip_testing_data

            2 test_array:
                  to check if the array which jpg show is right,it will just show the jpg array


      4 label:

            (to read tja and print out the label list)

            1 tjaread:
                  this tjaread will read the tja and cut the list with nothing at the beginning and end,and it will also maginfy the list smaller than 16 ,and it will turn [] to "0000000000000000"
                        ->["1223123010223021","0000000000000000","1223123010223021"] (it won't have "0000000000000000" at beginning and end)

            2 bk:
                  this file will change tjaread output list to single label list()
                        ["1223123010223021"] -> ["1","2","2", ... ,"1"]


      5 compression:

            (to zip list to tfrecords file)

            1 compression_filepath:
                  this file you need to input fft image filepath list and label list to this file then it will ouput tfrecords file,and if image it use out it will use a whiteimage which put in v2/data/white_image.jpg to mean no more song  (label part is in filling)

                  file packet:
                  {'height': _int64_feature(height),
                  'width': _int64_feature(width),
                  'depth': _int64_feature(depth),
                  'image_string': _bytes_feature(image_string),
                  'label': _int64_feature(label)}

                        ->v2\data\tfrecords

            2 decompression:
                  this file will unpacket the tfrecords file

            3 filling:(補齊)
                  . if label is not enough to the largest piece of entire training song it will fill in -1 to mean no more song
                  . count the biggest piece in training song

            4 white_picture:
                  to make a all white image which have 600*400 wieght and high 
                        -> v2\data\white_image.jpg

            5 /test/compression_file:
                  to make a tfrecords file by each image and its label

            6 /test/Overlay:
                  to read all tfrecords and put the data in a new list and combine to a big tfrecords

                  # maybe it can't use because combine list need large Ram,you can try


      6 data:
      
            (all kind of data is inside)

            1 level 6~7:
                  song in level 6~7

            2 split_ogg:
                  small piece of each song

            3 zip_testing_data:
                  jpg after fft

            4 tfrecords:
                  tfrecords file
            
            5 nosong.jpg:
                  when song don't have any song it fft jpg file,maybe can add at the end of each song cut

            6 white_image.jpg:
                  when no song need to fill with this and zip the tfrecords file
                  # if you have read the whole readme say TAT to me   by:2025/03/09 BU



# quote
      1 re
      https://chwang12341.medium.com/%E7%B5%A6%E8%87%AA%E5%B7%B1%E7%9A%84python%E5%B0%8F%E7%AD%86%E8%A8%98-%E5%BC%B7%E5%A4%A7%E7%9A%84%E6%95%B8%E6%93%9A%E8%99%95%E7%90%86%E5%B7%A5%E5%85%B7-%E6%AD%A3%E5%89%87%E8%A1%A8%E9%81%94%E5%BC%8F-regular-expression-regex%E8%A9%B3%E7%B4%B0%E6%95%99%E5%AD%B8-a5d20341a0b2

      2 tja file meaning
      https://github.com/269Seahorse/Better-taiko-web/blob/master/TJA-format.mediawiki#user-content-OFFSET
