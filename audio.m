filename = 'feroze_song.mp3';
[y,Fs] = audioread(filename);

% sound(y,Fs);

[pks, locs] = findpeaks(y(:,1), 'MinPeakDistance',Fs/10);

size(locs)

locs/Fs
