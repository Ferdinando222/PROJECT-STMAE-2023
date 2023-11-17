/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#pragma once

#include <JuceHeader.h>
#include "PluginProcessor.h"
#include "Library.h"
#include "CustomKnob.h"

//==============================================================================
/**
*/
class NeuralPluginAudioProcessorEditor  : public juce::AudioProcessorEditor,
                                          public juce::Button::Listener
{
public:
    NeuralPluginAudioProcessorEditor (NeuralPluginAudioProcessor&);
    ~NeuralPluginAudioProcessorEditor() override;

    //==============================================================================
    void paint (juce::Graphics&) override;
    void resized() override;
    void buttonClicked(juce::Button* button) override;
    void setBackground(juce::Colour colour);





private:
    // This reference is provided as a quick way for your editor to
    // access the processor object that created it.
    NeuralPluginAudioProcessor& audioProcessor;

    CustomKnob* knob1 = new CustomKnob("volume",audioProcessor);
    CustomKnob* knob2 = new CustomKnob("tone",audioProcessor);
    CustomKnob* knob3 = new CustomKnob("distortion",audioProcessor);

    juce::TextButton open;
    juce::TextButton save;
    juce::File selectedFile;
    juce::Label knobLabel1, knobLabel2, knobLabel3;
    juce::Colour backgroundColour;
    Library library;


 

    JUCE_DECLARE_NON_COPYABLE_WITH_LEAK_DETECTOR (NeuralPluginAudioProcessorEditor)
};
