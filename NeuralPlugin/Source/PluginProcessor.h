#pragma once
#include <JuceHeader.h>
#include <RTNeural/RTNeural.h>

namespace fs = std::filesystem;


class NeuralPluginAudioProcessor : public juce::AudioProcessor

{
public:
    //==============================================================================
    NeuralPluginAudioProcessor();
    ~NeuralPluginAudioProcessor() override;

    //==============================================================================
    void prepareToPlay(double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;
    bool isBusesLayoutSupported(const BusesLayout& layouts) const override;
    void processBlock(AudioBuffer<float>&, MidiBuffer&) override;
    //==============================================================================
    AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram(int index) override;
    const String getProgramName(int index) override;
    void changeProgramName(int index, const String& newName) override;

    //==============================================================================
    void getStateInformation(MemoryBlock& destData) override;
    void setStateInformation(const void* data, int sizeInBytes) override;
    void setValueKnob1(float knob_value);
    void setValueKnob2(float knob_value);
    void setValueKnob3(float knob_value);
    

private:
    //==============================================================================
    juce::AudioProcessorValueTreeState parameters;
    std::atomic<float>* inGainDbParam = nullptr;
    dsp::Gain<float> inputGain;
    dsp::ProcessorDuplicator<dsp::IIR::Filter<float>, dsp::IIR::Coefficients<float>> dcBlocker;


    float knob_value1 = 0.0f;
    float knob_value2 = 0.0f;
    float knob_value3 = 0.0f;
    // models
    std::atomic<float>* modelTypeParam = nullptr;
    std::unique_ptr<RTNeural::Model<float>> models[2];
    // example of model defined at compile-time

   
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(NeuralPluginAudioProcessor)
};