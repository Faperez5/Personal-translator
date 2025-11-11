// API Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State management
let state = {
    documentId: null,
    originalText: null,
    translatedText: null,
    segments: [],
    phrases: [],  // Phrase-level segments for highlighting
    currentPhraseIndex: 0,
    currentSegmentIndex: 0,
    audioElements: [],
    isPlaying: false,
    targetLanguage: 'es',
    phraseTimings: []  // Estimated timings for each phrase
};

// DOM Elements
const pdfFileInput = document.getElementById('pdf-file');
const uploadArea = document.getElementById('upload-area');
const uploadStatus = document.getElementById('upload-status');
const documentInfo = document.getElementById('document-info');
const translateBtn = document.getElementById('translate-btn');
const translateStatus = document.getElementById('translate-status');
const generateAudioBtn = document.getElementById('generate-audio-btn');
const audioStatus = document.getElementById('audio-status');
const audioPlayerContainer = document.getElementById('audio-player-container');
const textDisplay = document.getElementById('text-display');
const textContentOriginal = document.getElementById('text-content-original');
const textContentTranslated = document.getElementById('text-content-translated');
const playBtn = document.getElementById('play-btn');
const pauseBtn = document.getElementById('pause-btn');
const progressBar = document.getElementById('progress-bar');
const currentTimeSpan = document.getElementById('current-time');
const totalTimeSpan = document.getElementById('total-time');
const speedSelect = document.getElementById('speed');
const targetLangSelect = document.getElementById('target-lang');
const translationEditor = document.getElementById('translation-editor');
const translatedTextEditor = document.getElementById('translated-text-editor');
const editorCharCount = document.getElementById('editor-char-count');
const retranslateLangSelect = document.getElementById('retranslate-lang');
const retranslateBtn = document.getElementById('retranslate-btn');
const saveEditsBtn = document.getElementById('save-edits-btn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // File upload
    pdfFileInput.addEventListener('change', handleFileSelect);
    uploadArea.addEventListener('click', () => pdfFileInput.click());
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Translation
    translateBtn.addEventListener('click', handleTranslate);
    targetLangSelect.addEventListener('change', (e) => {
        state.targetLanguage = e.target.value;
    });

    // Audio generation
    generateAudioBtn.addEventListener('click', handleGenerateAudio);

    // Audio controls
    playBtn.addEventListener('click', handlePlay);
    pauseBtn.addEventListener('click', handlePause);
    speedSelect.addEventListener('change', handleSpeedChange);

    // Editor controls
    translatedTextEditor.addEventListener('input', updateCharCount);
    retranslateBtn.addEventListener('click', handleRetranslate);
    saveEditsBtn.addEventListener('click', handleSaveEdits);
}

// File Upload Handlers
function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        uploadFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');

    const file = event.dataTransfer.files[0];
    if (file && file.type === 'application/pdf') {
        uploadFile(file);
    } else {
        showStatus(uploadStatus, 'error', 'Please upload a PDF file');
    }
}

async function uploadFile(file) {
    showStatus(uploadStatus, 'loading', 'Uploading and extracting text from PDF...');

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch(`${API_BASE_URL}/upload`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            state.documentId = data.document_id;

            showStatus(uploadStatus, 'success', `File uploaded successfully! Extracted ${data.total_chars} characters from ${data.total_pages} pages.`);

            // Show document info
            documentInfo.classList.remove('hidden');
            documentInfo.innerHTML = `
                <h3>Document Information</h3>
                <p><strong>Filename:</strong> ${data.filename}</p>
                <p><strong>Pages:</strong> ${data.total_pages}</p>
                <p><strong>Characters:</strong> ${data.total_chars.toLocaleString()}</p>
            `;

            // Enable translation button
            translateBtn.disabled = false;
        } else {
            showStatus(uploadStatus, 'error', data.error || 'Upload failed');
        }
    } catch (error) {
        showStatus(uploadStatus, 'error', `Error: ${error.message}`);
    }
}

// Translation Handlers
async function handleTranslate() {
    if (!state.documentId) {
        showStatus(translateStatus, 'error', 'Please upload a PDF first');
        return;
    }

    const sourceLang = document.getElementById('source-lang').value;
    const targetLang = document.getElementById('target-lang').value;

    showStatus(translateStatus, 'loading', 'Translating document...');
    translateBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/translate/document`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: state.documentId,
                source_lang: sourceLang,
                target_lang: targetLang,
                service: 'google'
            })
        });

        const data = await response.json();

        if (data.success) {
            state.originalText = data.translation.original_text || '';
            state.translatedText = data.translation.translated_text || data.translation.full_text;

            showStatus(translateStatus, 'success', `Translation complete! Translated to ${targetLang.toUpperCase()}`);

            // Show editor with translated text
            translationEditor.classList.remove('hidden');
            translatedTextEditor.value = state.translatedText;
            retranslateLangSelect.value = targetLang;
            updateCharCount();

            // Enable audio generation
            generateAudioBtn.disabled = false;

            // Display translated text preview
            const preview = state.translatedText.substring(0, 500) + '...';
            translateStatus.innerHTML += `<div style="margin-top: 10px; padding: 10px; background: white; border-radius: 4px;"><strong>Preview:</strong><br>${preview}</div>`;
        } else {
            showStatus(translateStatus, 'error', data.error || 'Translation failed');
            translateBtn.disabled = false;
        }
    } catch (error) {
        showStatus(translateStatus, 'error', `Error: ${error.message}`);
        translateBtn.disabled = false;
    }
}

// Translation Editor Handlers
function updateCharCount() {
    const charCount = translatedTextEditor.value.length;
    editorCharCount.textContent = `${charCount.toLocaleString()} characters`;
}

async function handleRetranslate() {
    if (!state.documentId || !state.originalText) {
        showStatus(translateStatus, 'error', 'Please upload and translate a document first');
        return;
    }

    const sourceLang = document.getElementById('source-lang').value;
    const newTargetLang = retranslateLangSelect.value;

    showStatus(translateStatus, 'loading', 'Re-translating to ' + newTargetLang.toUpperCase() + '...');
    retranslateBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE_URL}/translate/document`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: state.documentId,
                source_lang: sourceLang,
                target_lang: newTargetLang,
                service: 'google'
            })
        });

        const data = await response.json();

        if (data.success) {
            state.translatedText = data.translation.translated_text || data.translation.full_text;
            state.targetLanguage = newTargetLang;

            // Update editor
            translatedTextEditor.value = state.translatedText;
            updateCharCount();

            showStatus(translateStatus, 'success', `Re-translated to ${newTargetLang.toUpperCase()}!`);

            // Update target language dropdown
            targetLangSelect.value = newTargetLang;

            // Reset audio (needs regeneration)
            generateAudioBtn.disabled = false;
            audioPlayerContainer.classList.add('hidden');
            textDisplay.classList.add('hidden');
        } else {
            showStatus(translateStatus, 'error', data.error || 'Re-translation failed');
        }
    } catch (error) {
        showStatus(translateStatus, 'error', `Error: ${error.message}`);
    } finally {
        retranslateBtn.disabled = false;
    }
}

function handleSaveEdits() {
    const editedText = translatedTextEditor.value.trim();

    if (!editedText) {
        showStatus(translateStatus, 'error', 'Text cannot be empty');
        return;
    }

    // Save edited text to state
    state.translatedText = editedText;

    showStatus(translateStatus, 'success', 'Edits saved! You can now generate audio with your changes.');

    // Reset audio (needs regeneration with new text)
    generateAudioBtn.disabled = false;
    audioPlayerContainer.classList.add('hidden');
    textDisplay.classList.add('hidden');
}

// Audio Generation Handlers
async function handleGenerateAudio() {
    if (!state.documentId || !state.translatedText) {
        showStatus(audioStatus, 'error', 'Please translate the document first');
        return;
    }

    showStatus(audioStatus, 'loading', 'Generating audio with sentence segments... This may take a moment.');
    generateAudioBtn.disabled = true;

    try {
        // Use edited text from editor or state
        const textToSpeak = translatedTextEditor.value.trim() || state.translatedText;

        const response = await fetch(`${API_BASE_URL}/tts/generate-custom`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                document_id: state.documentId,
                translated_text: textToSpeak,
                original_text: state.originalText,
                language: state.targetLanguage,
                service: 'gtts',
                segment_type: 'sentence'
            })
        });

        const data = await response.json();

        if (data.success) {
            state.segments = data.segments;

            showStatus(audioStatus, 'success', `Audio generated successfully! ${data.total_segments} segments created.`);

            // Setup audio player
            setupAudioPlayer();

            // Display text with segments
            displayTextWithSegments();

            // Show player and text display
            audioPlayerContainer.classList.remove('hidden');
            textDisplay.classList.remove('hidden');
        } else {
            showStatus(audioStatus, 'error', data.error || 'Audio generation failed');
            generateAudioBtn.disabled = false;
        }
    } catch (error) {
        showStatus(audioStatus, 'error', `Error: ${error.message}`);
        generateAudioBtn.disabled = false;
    }
}

// Audio Player Setup
function setupAudioPlayer() {
    let loadedCount = 0;
    const totalAudios = state.segments.filter(s => s.audio_path).length;

    // Create audio elements for each segment
    state.audioElements = state.segments.map(segment => {
        if (segment.audio_path) {
            const audio = new Audio();
            const filename = segment.audio_path.split('\\').pop().split('/').pop();
            audio.src = `${API_BASE_URL}/tts/audio/${state.documentId}/${filename}`;
            audio.playbackRate = parseFloat(speedSelect.value);

            // Add event listeners
            audio.addEventListener('ended', () => {
                playNextSegment();
            });

            audio.addEventListener('timeupdate', () => {
                updateProgress();
            });

            // Recalculate timings when audio metadata is loaded
            audio.addEventListener('loadedmetadata', () => {
                loadedCount++;
                // Once all audio files have loaded metadata, recalculate timings
                if (loadedCount === totalAudios) {
                    state.phraseTimings = calculatePhraseTiming();
                    console.log('Phrase timings recalculated with actual audio durations');
                }
            });

            return audio;
        }
        return null;
    }).filter(audio => audio !== null);
}

// Split text into phrases (3-5 words each)
function splitIntoPhrases(text, wordsPerPhrase = 4) {
    if (!text) return [];

    const words = text.split(/\s+/).filter(w => w.length > 0);
    const phrases = [];

    for (let i = 0; i < words.length; i += wordsPerPhrase) {
        const phraseWords = words.slice(i, i + wordsPerPhrase);
        phrases.push(phraseWords.join(' '));
    }

    return phrases;
}

// Create phrase segments from sentence segments
function createPhraseSegments() {
    const phrases = [];
    let phraseId = 0;

    state.segments.forEach((segment, segmentIndex) => {
        const translatedPhrases = splitIntoPhrases(segment.text || '');
        const originalPhrases = splitIntoPhrases(segment.original_text || '');

        // Match phrases count (use the longer one as reference)
        const maxPhrases = Math.max(translatedPhrases.length, originalPhrases.length);

        for (let i = 0; i < maxPhrases; i++) {
            phrases.push({
                id: phraseId++,
                segmentIndex: segmentIndex,
                translatedText: translatedPhrases[i] || '',
                originalText: originalPhrases[i] || '',
                phraseIndexInSegment: i
            });
        }
    });

    return phrases;
}

// Estimate timing for each phrase within segments
function calculatePhraseTiming() {
    const timings = [];

    state.phrases.forEach((phrase, phraseIndex) => {
        const segment = state.segments[phrase.segmentIndex];
        if (!segment || !state.audioElements[phrase.segmentIndex]) return;

        const audio = state.audioElements[phrase.segmentIndex];
        const segmentPhrases = state.phrases.filter(p => p.segmentIndex === phrase.segmentIndex);
        const phraseCount = segmentPhrases.length;

        // Use actual audio duration if available, otherwise estimate
        let segmentDuration;
        if (audio.duration && !isNaN(audio.duration) && audio.duration > 0) {
            // Use actual audio duration for accurate timing
            segmentDuration = audio.duration;
        } else {
            // Fall back to estimation (120 words per minute for more conservative estimate)
            const wordCount = (segment.text || '').split(/\s+/).length;
            segmentDuration = (wordCount / 120) * 60; // seconds
        }

        // Divide equally among phrases
        const phraseDuration = segmentDuration / phraseCount;
        const startTime = phrase.phraseIndexInSegment * phraseDuration;
        const endTime = startTime + phraseDuration;

        timings.push({
            phraseIndex,
            segmentIndex: phrase.segmentIndex,
            startTime,
            endTime,
            duration: phraseDuration
        });
    });

    return timings;
}

// Display Text with Segments (Dual Panel)
function displayTextWithSegments() {
    textContentOriginal.innerHTML = '';
    textContentTranslated.innerHTML = '';

    // Create phrase-level segments
    state.phrases = createPhraseSegments();
    state.phraseTimings = calculatePhraseTiming();

    // Render phrases in both panels
    state.phrases.forEach((phrase, index) => {
        // Original text panel
        if (phrase.originalText) {
            const originalSpan = document.createElement('span');
            originalSpan.className = 'phrase';
            originalSpan.textContent = phrase.originalText + ' ';
            originalSpan.dataset.index = index;

            originalSpan.addEventListener('click', () => {
                seekToPhrase(index);
            });

            textContentOriginal.appendChild(originalSpan);
        }

        // Translated text panel
        if (phrase.translatedText) {
            const translatedSpan = document.createElement('span');
            translatedSpan.className = 'phrase';
            translatedSpan.textContent = phrase.translatedText + ' ';
            translatedSpan.dataset.index = index;

            translatedSpan.addEventListener('click', () => {
                seekToPhrase(index);
            });

            textContentTranslated.appendChild(translatedSpan);
        }
    });

    // Setup synchronized scrolling
    setupSynchronizedScrolling();
}

// Playback Controls
function handlePlay() {
    if (state.audioElements.length === 0) return;

    state.isPlaying = true;
    playBtn.classList.add('hidden');
    pauseBtn.classList.remove('hidden');

    playCurrentSegment();
}

function handlePause() {
    state.isPlaying = false;
    pauseBtn.classList.add('hidden');
    playBtn.classList.remove('hidden');

    if (state.audioElements[state.currentSegmentIndex]) {
        state.audioElements[state.currentSegmentIndex].pause();
    }
}

function playCurrentSegment() {
    if (!state.isPlaying) return;

    const currentAudio = state.audioElements[state.currentSegmentIndex];
    if (currentAudio) {
        currentAudio.play();
        // Start phrase-level highlighting for this segment
        startPhraseHighlighting(state.currentSegmentIndex);
    }
}

function playNextSegment() {
    state.currentSegmentIndex++;

    if (state.currentSegmentIndex < state.audioElements.length) {
        playCurrentSegment();
    } else {
        // Reached end
        handlePause();
        state.currentSegmentIndex = 0;
        removeAllHighlights();
    }
}

function seekToPhrase(phraseIndex) {
    const phrase = state.phrases[phraseIndex];
    if (!phrase) return;

    // Pause current playback
    if (state.isPlaying) {
        if (state.audioElements[state.currentSegmentIndex]) {
            state.audioElements[state.currentSegmentIndex].pause();
            state.audioElements[state.currentSegmentIndex].currentTime = 0;
        }
    }

    // Update indices
    state.currentSegmentIndex = phrase.segmentIndex;
    state.currentPhraseIndex = phraseIndex;

    // Start playing from new position if was playing
    if (state.isPlaying) {
        playCurrentSegment();
    } else {
        highlightPhrase(phraseIndex);
    }
}

// Start phrase-level highlighting for current segment
function startPhraseHighlighting(segmentIndex) {
    const segmentPhrases = state.phrases.filter(p => p.segmentIndex === segmentIndex);
    if (segmentPhrases.length === 0) return;

    const audio = state.audioElements[segmentIndex];
    if (!audio) return;

    // Track audio time and update phrase highlighting
    const updateHighlight = () => {
        if (state.currentSegmentIndex !== segmentIndex || !state.isPlaying) return;

        const currentTime = audio.currentTime;
        const timing = state.phraseTimings.find(t =>
            t.segmentIndex === segmentIndex &&
            currentTime >= t.startTime &&
            currentTime < t.endTime
        );

        if (timing && timing.phraseIndex !== state.currentPhraseIndex) {
            state.currentPhraseIndex = timing.phraseIndex;
            highlightPhrase(timing.phraseIndex);
        }

        if (state.isPlaying && state.currentSegmentIndex === segmentIndex) {
            requestAnimationFrame(updateHighlight);
        }
    };

    requestAnimationFrame(updateHighlight);
}

function handleSpeedChange(event) {
    const speed = parseFloat(event.target.value);
    state.audioElements.forEach(audio => {
        audio.playbackRate = speed;
    });
}

// Visual Feedback - Highlight phrases in both panels
function highlightPhrase(phraseIndex) {
    // Remove previous highlights
    removeAllHighlights();

    // Highlight in both panels
    const originalPhrases = textContentOriginal.querySelectorAll('.phrase');
    const translatedPhrases = textContentTranslated.querySelectorAll('.phrase');

    if (originalPhrases[phraseIndex]) {
        originalPhrases[phraseIndex].classList.add('active');
        originalPhrases[phraseIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    if (translatedPhrases[phraseIndex]) {
        translatedPhrases[phraseIndex].classList.add('active');
        translatedPhrases[phraseIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function removeAllHighlights() {
    const originalPhrases = textContentOriginal.querySelectorAll('.phrase');
    const translatedPhrases = textContentTranslated.querySelectorAll('.phrase');

    originalPhrases.forEach(phrase => {
        phrase.classList.remove('active');
    });

    translatedPhrases.forEach(phrase => {
        phrase.classList.remove('active');
    });
}

// Progress Updates
function updateProgress() {
    const currentAudio = state.audioElements[state.currentSegmentIndex];
    if (!currentAudio) return;

    // Calculate overall progress
    const totalSegments = state.audioElements.length;
    const segmentProgress = state.currentSegmentIndex / totalSegments;
    const currentSegmentProgress = (currentAudio.currentTime / currentAudio.duration) / totalSegments;
    const totalProgress = (segmentProgress + currentSegmentProgress) * 100;

    progressBar.style.width = `${totalProgress}%`;

    // Update time display
    currentTimeSpan.textContent = formatTime(currentAudio.currentTime);
    if (currentAudio.duration) {
        totalTimeSpan.textContent = formatTime(currentAudio.duration);
    }
}

// Utility Functions
function showStatus(element, type, message) {
    element.className = `status-message show ${type}`;

    if (type === 'loading') {
        element.innerHTML = `<span class="spinner"></span>${message}`;
    } else {
        element.textContent = message;
    }
}

function formatTime(seconds) {
    if (!seconds || isNaN(seconds)) return '0:00';

    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}

// Synchronized Scrolling between panels
function setupSynchronizedScrolling() {
    let isScrolling = false;

    const syncScroll = (source, target) => {
        if (isScrolling) return;
        isScrolling = true;

        const scrollPercentage = source.scrollTop / (source.scrollHeight - source.clientHeight);
        target.scrollTop = scrollPercentage * (target.scrollHeight - target.clientHeight);

        setTimeout(() => {
            isScrolling = false;
        }, 50);
    };

    textContentOriginal.addEventListener('scroll', () => {
        syncScroll(textContentOriginal, textContentTranslated);
    });

    textContentTranslated.addEventListener('scroll', () => {
        syncScroll(textContentTranslated, textContentOriginal);
    });
}

// Error handling
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
