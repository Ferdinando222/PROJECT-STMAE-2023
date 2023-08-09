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

    // Create and configure knobs with labels
    addAndMakeVisible(knob1);
    knob1.setRange(0, 1);

    addAndMakeVisible(knob2);
    knob2.setRange(0, 1);

    addAndMakeVisible(knob3);
    knob3.setRange(0, 1);

    // Set knob styles and listeners
    knob1.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob1.addListener(this);

    knob2.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob2.addListener(this);

    knob3.setSliderStyle(juce::Slider::RotaryHorizontalDrag);
    knob3.addListener(this);

    // Attach labels to knobs

    // Add labels to the main component
    addAndMakeVisible(knobLabel1);
    addAndMakeVisible(knobLabel2);
    addAndMakeVisible(knobLabel3);

    // Set label texts
    knobLabel1.setText("Volume", juce::NotificationType::dontSendNotification);
    knobLabel2.setText("Tone", juce::NotificationType::dontSendNotification);
    knobLabel3.setText("Saturation", juce::NotificationType::dontSendNotification);
  
    knobLabel1.attachToComponent(&knob1, false);
    knobLabel2.attachToComponent(&knob2, false);
    knobLabel3.attachToComponent(&knob3, false);


    // Create and configure an "Open Model" button
    addAndMakeVisible(open);
    open.addListener(this);
    open.setButtonText("Open Model");


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


    // Position the knobs horizontally at the top
    knob1.setBounds(0, getHeight()/3, getWidth() / 3, rowHeight * 1.5);
    knob2.setBounds(getWidth() / 3, getHeight()/3, getWidth() / 3, rowHeight * 1.5);
    knob3.setBounds(getWidth() * 2 / 3, getHeight()/3, getWidth() / 3, rowHeight * 1.5);

    // Position the "Open" button centered at the bottom
    open.setBounds(getWidth() / 4, getHeight() - rowHeight * 1.5, getWidth() / 2, rowHeight * 1.5);
}

void NeuralPluginAudioProcessorEditor::buttonClicked(juce::Button* button)
{
    if(button == &open)
    {
        juce::FileChooser fileChooser("Select a file to open...",
            juce::File::getSpecialLocation(juce::File::userHomeDirectory),
            "*.json*");

        if (fileChooser.browseForFileToOpen())
        {
            juce::File selectedFile = fileChooser.getResult();
            juce::AlertWindow::showMessageBoxAsync(juce::AlertWindow::InfoIcon,
                "File Selected",
                "You selected the file:\n" + selectedFile.getFullPathName());
            auto path = selectedFile.getFullPathName().toRawUTF8();
            audioProcessor.setFilePath(path);
        }
    }

}

