function speech_analitics(audio_path,gender,truthfulness,distance_speech,distance_inter_speech,tinc_pitch)
    %Obtener la onda de audio a partir del archivo
    [speech,fs] = audioread(audio_path);
    speech=speech(:,1);
    speech = speech./max(abs(speech));
    switch nargin
        case 3
            distance_speech=1;
            distance_inter_speech=0.5;
            tinc_pitch=0.05;
        case 4
            distance_inter_speech=0.5;
            tinc_pitch=0.05;
        case 5
            tinc_pitch=0.05;
    end
    t = (0:size(speech,1)-1)/fs;
    
    mergedistance=fs*distance_speech; %Si la separación entre audios es menor a 1 segundos se unirán
    
    %Segmentar las zonas con discurso
    VADidx = detectSpeech(speech,fs,"MergeDistance",mergedistance);
    speech_rate=zeros(1,length(speech));
    E=zeros(1,length(speech));
    pauses=zeros(1,length(speech));
    idx_pauses=1;
    VADidx_inter_cell=cell(1);
    VADidx_inter_cell_idx=1;
    tuple_pauses=cell(1);
    tuple_pauses{1}={'Time', 0,'Pause_Duration', 0};

    %Para cada zona segmentada extraer caracteristicas (pitch, speech rate,
    %energy y pausas)
    for i=1:size(VADidx,1)
        inter=VADidx(i,:);
        t1=inter(1)/fs;
        t2=inter(2)/fs;
        E(inter(1):inter(2))=v_teager(speech(inter(1):inter(2)));
        if t2-t1 <3
            landm=landmarks(speech(inter(1):inter(2)),fs);
            speech_rate(inter(1):inter(2))=lm_syl_count(landm)/(t2-t1);
        else
            
            mergedistance_inter=distance_inter_speech*fs; %Si la separación entre audios es menor a 500ms, los audios se unirán
    
            VADidx_inter = detectSpeech(speech(inter(1):inter(2)),fs,"MergeDistance",mergedistance_inter,"Thresholds",[0.2,0]);
            VADidx_inter_cell{VADidx_inter_cell_idx}=VADidx_inter;
            VADidx_inter_cell_idx=VADidx_inter_cell_idx+1;
            for j=1:size(VADidx_inter,1)
                t1_inter=(inter(1)+VADidx_inter(j,1))/fs;
                t2_inter=(inter(1)+VADidx_inter(j,2))/fs;
                if t2_inter-t1_inter>=1 %Si el intervalo de audio es mayor a 1s, entonces realizar calculos para obtener el speech Rate
                    landm=landmarks(speech(inter(1)+VADidx_inter(j,1):inter(1)+VADidx_inter(j,2)),fs);
                    speech_rate(inter(1)+VADidx_inter(j,1):inter(1)+VADidx_inter(j,2))=lm_syl_count(landm)/(t2_inter-t1_inter);
                end
                
                if j+1<=size(VADidx_inter,1)
                    pauses(inter(1)+VADidx_inter(j,1):inter(1)+VADidx_inter(j,2))=((inter(1)+VADidx_inter(j+1,1))-(inter(1)+VADidx_inter(j,2)))/fs;
                    fin_pause=(inter(1)+VADidx_inter(j+1,1))/fs;
                    inic_pause=(inter(1)+VADidx_inter(j,2))/fs;
                    tuple_pauses{idx_pauses}={'Time', [round(inic_pause,2) round(fin_pause,2)], 'Pause_Duration', round(fin_pause-inic_pause,2)};
                    idx_pauses=idx_pauses+1;
                end
                
            end
        end
        
    end
    [pitch,tx]=v_fxpefac(speech,fs,tinc_pitch);

    %Generar las figuras con las caracteristicas extraidas a lo largo del
    %audio
    h=figure('Visible','Off');
    detectSpeech(speech,fs,"MergeDistance",mergedistance)
    title("Speech Detection")
    xlabel("Time (s)")
    ylabel("Amplitude")
    name=strsplit(audio_path,{'/','.'});
    name=name(4);
    folder="Figures/";
    saveas(h,folder+name+"_Speech_Detection.png")

    h=figure('Visible','Off');
    plot(t,speech_rate)
    normal_speech_rate=zeros(1,length(speech_rate));
    high_speech_rate=zeros(1,length(speech_rate));
    low_speech_rate=zeros(1,length(speech_rate));
    low_speech_rate(1:end)=3.5;
    normal_speech_rate(1:end)=4;
    high_speech_rate(1:end)=4.5;
    line(t,low_speech_rate,'Color','red','LineStyle','--')
    line(t,normal_speech_rate,'Color','green','LineStyle','--')
    line(t,high_speech_rate,'Color','red','LineStyle','--')
    title("Speech Rate")
    xlabel("Time (s)")
    ylabel("Speech Rate (syll/sec)")
    xlim([t(1),t(end)])
    saveas(h,folder+name+"_Speech_Rate.png")

    h=figure('Visible','Off');
    plot(tx,pitch)
    high_pitch=zeros(1,length(speech_rate));
    low_pitch=zeros(1,length(speech_rate));
    if gender=="male"
        high_pitch(1:end)=180;
        line(t,high_pitch,'Color','red','LineStyle','--')
        low_pitch(1:end)=85;
        line(t,low_pitch,'Color','red','LineStyle','--')
        line(t,(high_pitch+low_pitch)/2,'Color','green','LineStyle','--')
        title("Male Pitch Detection")
    elseif gender=="female"
        high_pitch(1:end)=255;
        line(t,high_pitch,'Color','red','LineStyle','--')
        low_pitch(1:end)=165;
        line(t,low_pitch,'Color','red','LineStyle','--')
        line(t,(high_pitch+low_pitch)/2,'Color','green','LineStyle','--')
        title("Female Pitch Detection")
    end
    xlabel("Time (s)")
    ylabel("Pitch (Hz)")
    axis tight
    saveas(h,folder+name+"_Speech_Pitch.png")
    
    h=figure('Visible','Off');
    plot(t,E)
    title("Energy speech")
    xlabel("Time (s)")
    ylabel("Energy")
    axis tight
    saveas(h,folder+name+"_Speech_Energy.png")

    h=figure('Visible','Off');
    plot(t,pauses)
    title("Pauses speech")
    xlabel("Time (s)")
    ylabel("Time pauses(s)")
    axis tight
    saveas(h,folder+name+"_Speech_Pauses.png")

    % Guardar los datos de las caracteristicas extraidas
    idx_tmp=1;
    tuple_clasification=cell(1);
    idx_tuple=1;
    for i=1:size(VADidx,1)
        inter=VADidx(i,:);
        t1=inter(1)/fs;
        t2=inter(2)/fs;
        if t2-t1>3
           tmp=VADidx_inter_cell{idx_tmp};
           idx_tmp=idx_tmp+1;
           for j=1:size(tmp,1)
               t1_inter=(VADidx(i,1)+tmp(j,1))/fs;
               t2_inter=(VADidx(i,1)+tmp(j,2))/fs;
               a=sort(tx(:));
               ini_tx=interp1(a,a,t1_inter,'nearest');
               fin_tx=interp1(a,a,t2_inter,'nearest');
               
               if t2_inter>a(end)
                   fin_tx=a(end);
               end
               idx_ini_pitch=find(tx==ini_tx);
               idx_fin_pitch=find(tx==fin_tx);
               mean_pitch=mean(pitch(idx_ini_pitch:idx_fin_pitch));
               mean_energy=mean(E(VADidx(i,1)+tmp(j,1):VADidx(i,1)+tmp(j,2)));
               mean_rate=speech_rate(VADidx(i,1)+tmp(j,1));
               tuple_clasification{idx_tuple}={'Time', [round(t1_inter,2) round(t2_inter,2)],'Pitch',round(mean_pitch,2),'Energy',mean_energy,'Speech_Rate', round(mean_rate,2)};
               idx_tuple=idx_tuple+1;
           end
      
        else
            a=sort(tx(:));
            ini_tx=interp1(a,a,t1,'nearest');
            fin_tx=interp1(a,a,t2,'nearest');
            
            if t2>a(end)
               fin_tx=a(end);
            end
            idx_ini_pitch=find(tx==ini_tx);
            idx_fin_pitch=find(tx==fin_tx);
            mean_pitch=mean(pitch(idx_ini_pitch:idx_fin_pitch));
            mean_energy=mean(E(VADidx(i,1):VADidx(i,2)));
            mean_rate=speech_rate(VADidx(i,1));
            tuple_clasification{idx_tuple}={'Time', [round(t1,2) round(t2,2)],'Pitch',round(mean_pitch,2),'Energy',mean_energy,'Speech_Rate', round(mean_rate,2)};
            idx_tuple=idx_tuple+1;
        end
    end

    fileID = fopen("DataFiles/"+name+".txt",'w');
    fprintf(fileID,'%s\n','El análisis de este audio muestra lo siguiente:');
    if gender=="male"
        fprintf(fileID,'%s\n','Se trata de la voz de un hombre, por tanto, su frecuencia de tono natural debe estar entre los 85 y 180 Hz');
        range_pitch=[85 180];
    elseif gender=="female"
        fprintf(fileID,'%s\n','Se trata de la voz de una mujer, por tanto, su frecuencia de tono natural debe estar entre los 165 y 255 Hz');
        range_pitch=[165 255];
    end
    fprintf(fileID,'%s %e\n','Su voz tiene una energía media de: ', mean(E));
    if tuple_pauses{1}{2}==0
        fprintf(fileID,'%s %.2f\n','Numero de Pausas realizadas: ', 0);
    else
        fprintf(fileID,'%s %.2f\n','Numero de Pausas realizadas: ', size(tuple_pauses,2));
    end
    if truthfulness
        fprintf(fileID,'%s\n\n','La persona de este audio está siendo sincera');
    else
        fprintf(fileID,'%s\n\n','La persona de este audio está mintiendo');
    end
    fprintf(fileID,'%s\n','Analisis Completo del espectro de audio:');
    fclose(fileID);
    
    for i=1:size(tuple_clasification,2)
        writecell(tuple_clasification{i},"DataFiles/"+name,'Delimiter','tab','WriteMode','append');
    end
    for i=1:size(tuple_pauses,2)
        writecell(tuple_pauses{i},"DataFiles/"+name,'Delimiter','tab','WriteMode','append');
    end
    name=erase(name,"_audio");
    dest_folder='../Gesture and emotion recognition/'+name+'/';
    if not(isfolder(dest_folder))
        mkdir(dest_folder)
    end
    save(dest_folder+'tuple_clasification.mat',"tuple_clasification","-v7")
    save(dest_folder+'tuple_pauses.mat',"tuple_pauses","-v7")
    analitics={'Range_Pitch', range_pitch, 'Truthfulness', truthfulness, 'Mean_Energy', mean(E), 'Range_velocity', [3.5 4.5]};
    save(dest_folder+'analitics.mat',"analitics","-v7")
    
end
    
    
    