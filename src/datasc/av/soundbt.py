import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sounddevice as sd
import queue

# Audio configuration
SAMPLE_RATE = 44100  # Sample rate
BLOCK_SIZE = 1024    # Block size for audio processing
CHANNELS = 1         # Mono audio

class AudioVisualizer:
    def __init__(self):
        # Queue for audio data
        self.audio_queue = queue.Queue()
        
        # Initialize plot
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(12, 8))
        self.fig.suptitle('Real-time Microphone Audio Visualization')
        
        # Time domain plot
        self.x_time = np.arange(0, BLOCK_SIZE)
        self.line_time, = self.ax1.plot(self.x_time, np.zeros(BLOCK_SIZE))
        self.ax1.set_ylim(-0.5, 0.5)
        self.ax1.set_xlim(0, BLOCK_SIZE)
        self.ax1.set_title('Time Domain (Waveform)')
        self.ax1.set_xlabel('Sample')
        self.ax1.set_ylabel('Amplitude')
        
        # Frequency domain plot
        self.x_freq = np.linspace(0, SAMPLE_RATE/2, BLOCK_SIZE//2)
        self.line_freq, = self.ax2.plot(self.x_freq, np.zeros(BLOCK_SIZE//2))
        self.ax2.set_ylim(0, 0.1)
        self.ax2.set_xlim(0, SAMPLE_RATE/2)
        self.ax2.set_title('Frequency Domain (Spectrum)')
        self.ax2.set_xlabel('Frequency (Hz)')
        self.ax2.set_ylabel('Magnitude')
        
        plt.tight_layout()
    
    def audio_callback(self, indata, frames, time, status):
        """Callback function for audio input"""
        if status:
            print(f"Audio status: {status}")
        
        # Put audio data in queue
        if not self.audio_queue.full():
            self.audio_queue.put(indata[:, 0].copy())  # Take first channel
    
    def update_plot(self, frame):
        """Update the plot with new audio data"""
        try:
            # Get latest audio data
            if not self.audio_queue.empty():
                audio_data = self.audio_queue.get()
                
                # Update time domain plot
                self.line_time.set_ydata(audio_data)
                
                # Calculate FFT for frequency domain
                fft = np.abs(np.fft.rfft(audio_data))
                fft = fft[:len(self.x_freq)]  # Ensure correct length
                
                # Update frequency domain plot
                self.line_freq.set_ydata(fft)
                
                # Auto-scale frequency plot
                if np.max(fft) > 0:
                    self.ax2.set_ylim(0, np.max(fft) * 1.1)
        
        except queue.Empty:
            pass
        except Exception as e:
            print(f"Error updating plot: {e}")
        
        return self.line_time, self.line_freq
    
    def start(self):
        """Start the visualization"""
        try:
            print("Available audio devices:")
            print(sd.query_devices())
            print("\nStarting audio visualization...")
            print("Speak into your microphone to see the waveform and spectrum!")
            print("Close the plot window to stop.")
            
            # Start audio stream
            with sd.InputStream(
                channels=CHANNELS,
                samplerate=SAMPLE_RATE,
                blocksize=BLOCK_SIZE,
                callback=self.audio_callback
            ):
                # Create animation
                ani = animation.FuncAnimation(
                    self.fig, 
                    self.update_plot, 
                    interval=50,  # Update every 50ms
                    blit=True,
                    cache_frame_data=False
                )
                
                plt.show()
            
        except KeyboardInterrupt:
            print("Stopping...")
        except Exception as e:
            print(f"Error: {e}")
            print("Make sure you have a microphone connected and permissions are granted.")

def main():
    # Create and start visualizer
    visualizer = AudioVisualizer()
    visualizer.start()

if __name__ == "__main__":
    main()