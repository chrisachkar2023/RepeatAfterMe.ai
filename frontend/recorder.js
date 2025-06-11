const recordBtn = document.getElementById('record-btn');
const status = document.getElementById('record-status');
const fileInput = document.getElementById('fileinput');
const audioPlayer = document.getElementById('audioPlayer');
const submitBtn = document.getElementById('submit-btn');
let recorder, chunks;

recordBtn.onclick = async () => {
if (recordBtn.textContent === 'Start Recording') {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        recorder = new MediaRecorder(stream);
        chunks = [];
        recorder.ondataavailable = e => chunks.push(e.data);
        recorder.start();
        recordBtn.textContent = 'Stop Recording';
        textContent = 'Recording...';
        submitBtn.disabled = true;
        audioPlayer.style.display = 'none';
        audioPlayer.src = '';
    } catch (e) {
        console.warn('Microphone access denied or not available.');
    }
} 

else {
    recorder.stop();
    recordBtn.textContent = 'Start Recording';
    textContent = 'Processing audio...';

    recorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/mp3' });
        const audioURL = URL.createObjectURL(blob);
        audioPlayer.src = audioURL;
        audioPlayer.style.display = 'block';
        textContent = 'Recording ready to upload. Submit the form.';

        // convert Blob to a File object and set it to the hidden file input
        const file = new File([blob], 'recording.mp3', { type: 'audio/mp3' });
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;

        submitBtn.disabled = false;
    };
}
};