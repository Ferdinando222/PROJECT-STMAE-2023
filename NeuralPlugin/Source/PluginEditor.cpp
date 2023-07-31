/*
  ==============================================================================

    This file contains the basic framework code for a JUCE plugin editor.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

//==============================================================================
NeuralPluginAudioProcessorEditor::NeuralPluginAudioProcessorEditor (NeuralPluginAudioProcessor& p)
    : AudioProcessorEditor (&p), audioProcessor (p)
{
    // Make sure that before the constructor has finished, you've set the
    // editor's size to whatever you need it to be.
    setSize(600, 500);
}

NeuralPluginAudioProcessorEditor::~NeuralPluginAudioProcessorEditor()
{
}

//==============================================================================
void NeuralPluginAudioProcessorEditor::paint (juce::Graphics& g)
{
    // (Our component is opaque, so we must completely fill the background with a solid colour)
    g.fillAll (getLookAndFeel().findColour (juce::ResizableWindow::backgroundColourId));

    g.setColour (juce::Colours::white);
    g.setFont (15.0f);

    addAndMakeVisible(knob1);
    knob1.setRange(0, 1);
    knob1.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob1.addListener(this);

    addAndMakeVisible(knob2);
    knob2.setRange(0, 1);
    knob2.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob2.addListener(this);

    addAndMakeVisible(knob3);
    knob3.setRange(0, 1);
    knob3.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob3.addListener(this);
}

void NeuralPluginAudioProcessorEditor::sliderValueChanged(juce::Slider* slider)
{
    if (slider == &knob1)
    {
        audioProcessor.setValueKnob1(float(knob1.getValue()));
    }

    if (slider == &knob2)
    {
        audioProcessor.setValueKnob2(float(knob2.getValue()));
    }

    if (slider == &knob3)
    {
        audioProcessor.setValueKnob3(float(knob3.getValue()));
    }

}

void NeuralPluginAudioProcessorEditor::resized()
{
    // This is generally where you'll want to lay out the positions of any
    // subcomponents in your editor..
    float rowHeight = getHeight() / 5;
    knob1.setBounds(getWidth() / 1.5, 0, getWidth() / 4, rowHeight * 1.5);
    knob2.setBounds(getWidth() / 2.5, 0, getWidth() / 4, rowHeight * 1.5);
    knob3.setBounds(getWidth() / 3.5, 0, getWidth() / 4, rowHeight * 1.5);
}

