class PeakWorkletProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this._buffer = [];
    this._time = 0;
  }

  process(inputs) {
    const input = inputs[0];
    const channel = input[0];

    if (channel) {
      let min = 1.0;
      let max = -1.0;

      for (let i = 0; i < channel.length; i++) {
        const sample = channel[i];
        if (sample < min) min = sample;
        if (sample > max) max = sample;
      }

      this._buffer.push({ min, max });
      this._time += channel.length / sampleRate;

      if (this._buffer.length >= 128) {
        this.port.postMessage({ min, max, time: this._time });
        this._buffer = [];
      }
    }

    return true;
  }
}

registerProcessor('peak-worklet-processor', PeakWorkletProcessor);
