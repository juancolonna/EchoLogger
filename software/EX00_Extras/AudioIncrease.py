WAV_FILE = "record_3.wav"
NEW_FILE = "louder.wav"
f = open(NEW_FILE,"wb")

def aumentar_volume(input_file, output_file, aumento):
    # Abre o arquivo WAV de entrada para leitura binária
    with open(input_file, 'rb') as file_in:
        # Lê o cabeçalho do arquivo
        header = file_in.read(44)  # Os primeiros 44 bytes contêm o cabeçalho do WAV

        # Lê os dados de áudio
        audio_data = bytearray(file_in.read())

    # Aumenta o volume multiplicando cada amostra pelo fator de aumento
    for i in range(0, len(audio_data), 2):  # Os dados de áudio são codificados em dois bytes (16 bits) por amostra
        sample = int.from_bytes(audio_data[i:i+2], byteorder='little', signed=True)
        new_sample = int(sample * aumento)
        new_sample = max(min(new_sample, 32767), -32768)  # Garante que o novo valor esteja no intervalo de um inteiro de 16 bits
        audio_data[i:i+2] = new_sample.to_bytes(2, byteorder='little', signed=True)

    # Abre o arquivo WAV de saída para escrita binária
    with open(output_file, 'wb') as file_out:
        # Escreve o cabeçalho do arquivo
        file_out.write(header)
        # Escreve os dados de áudio ajustados
        file_out.write(audio_data)

# Exemplo de uso
aumentar_volume(WAV_FILE, NEW_FILE, 10)  # Aumentar volume em 1000%
   
