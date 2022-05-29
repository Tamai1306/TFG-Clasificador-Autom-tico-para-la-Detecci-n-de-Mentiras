clear,close all,clc
folder="../Dataset/audio/";
list = importdata(folder+'lie_detection_wav.txt');
for i=1:size(list,1)
    data=strsplit(list{i});
    audio_path=folder+string(data{1});
    gender=data{2};
    truthfullness=str2num(data{3});
    disp("Analizando: "+string(data{1})+"...")
    speech_analitics(audio_path,gender,truthfullness);
    disp("Terminado")
end
