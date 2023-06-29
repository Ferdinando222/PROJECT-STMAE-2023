/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin processor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include <RTNeural/RTNeural.h>
#include <filesystem>
#include <iostream>

using ModelType = RTNeural::ModelT<float, 1, 1, RTNeural::LSTMLayerT<float, 1, 8>, RTNeural::DenseT<float, 8, 1>>;

//==============================================================================
/**
*/
class NeuralPluginAudioProcessor  : public juce::AudioProcessor
                            #if JucePlugin_Enable_ARA
                             , public juce::AudioProcessorARAExtension
                            #endif
{
public:
    //==============================================================================
    NeuralPluginAudioProcessor();
    ~NeuralPluginAudioProcessor() override;

    //==============================================================================
    void prepareToPlay (double sampleRate, int samplesPerBlock) override;
    void releaseResources() override;

   #ifndef JucePlugin_PreferredChannelConfigurations
    bool isBusesLayoutSupported (const BusesLayout& layouts) const override;
   #endif

    void processBlock (juce::AudioBuffer<float>&, juce::MidiBuffer&) override;

    //==============================================================================
    juce::AudioProcessorEditor* createEditor() override;
    bool hasEditor() const override;

    //==============================================================================
    const juce::String getName() const override;

    bool acceptsMidi() const override;
    bool producesMidi() const override;
    bool isMidiEffect() const override;
    double getTailLengthSeconds() const override;

    //==============================================================================
    int getNumPrograms() override;
    int getCurrentProgram() override;
    void setCurrentProgram (int index) override;
    const juce::String getProgramName (int index) override;
    void changeProgramName (int index, const juce::String& newName) override;

    //==============================================================================
    void getStateInformation (juce::MemoryBlock& destData) override;
    void setStateInformation (const void* data, int sizeInBytes) override;
    nlohmann::json get_model_json(std::filesystem::path json_file_path);
    void loadModel(nlohmann::json modelJson, ModelType& model);

private:
    //==============================================================================
    float raw_audio;
    nlohmann::json model_json;
    ModelType model;

    std::unique_ptr<RTNeural::Model<float>> neuralNet[2];
    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (NeuralPluginAudioProcessor)

};
