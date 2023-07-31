/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"

//==============================================================================
/**
*/
class NeuralPluginAudioProcessorEditor  : public juce::AudioProcessorEditor,
    
                                          public juce::Slider::Listener
{
public:
    NeuralPluginAudioProcessorEditor (NeuralPluginAudioProcessor&);
    ~NeuralPluginAudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void sliderValueChanged(juce::Slider* slider) override;
    void resized() override;


private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    NeuralPluginAudioProcessor& audioProcessor;
    juce::Slider knob1;
    juce::Slider knob2;
    juce::Slider knob3;

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (NeuralPluginAudioProcessorEditor)
};
