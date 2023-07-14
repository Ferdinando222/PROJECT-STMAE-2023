#pragma once
#include <JuceHeader.h>
#include <RTNeural/RTNeural.h>
using ModelType = RTNeural::ModelT<float, 1, 1, RTNeural::Conv1DT<float,1,1,3,1>, RTNeural::LSTMLayerT<float, 1, 8>, RTNeural::DenseT<float, 8, 1 >> ;
namespace fs = std::filesystem;


class NeuralPluginAudioProcessor : public AudioProcessor
{
public:
    //==============================================================================
    NeuralPluginAudioProcessor();
    ~NeuralPluginAudioProcessor();

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
    void loadModel(std::ifstream& jsonStream, ModelType& model);

private:
    //==============================================================================
    AudioProcessorValueTreeState parameters;

    // input gain
    std::atomic<float>* inGainDbParam = nullptr;
    dsp::Gain<float> inputGain;


    // models
    std::atomic<float>* modelTypeParam = nullptr;
    std::unique_ptr<RTNeural::Model<float>> models[2];
    // example of model defined at compile-time

    dsp::ProcessorDuplicator<dsp::IIR::Filter<float>, dsp::IIR::Coefficients<float>> dcBlocker;
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR(NeuralPluginAudioProcessor)
};