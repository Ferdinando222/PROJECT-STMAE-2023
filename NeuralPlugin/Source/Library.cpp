#include "Library.h"

Library::Library()
{
    setSize(20, 50);
    label.setText("LIBRARY", juce::dontSendNotification);
    label.setFont(juce::Font(16.0f, juce::Font::bold));
    label.setJustificationType(juce::Justification::centred);
    label.setColour(juce::Label::textColourId,juce::Colours::black);
    addAndMakeVisible(label);

}


void Library::paint(juce::Graphics& g)
{
    g.fillAll(Colours::lightgrey);
}

void Library::resized()
{
    int labelHeight = 30; 
    label.setBounds(0, 0, getWidth(), labelHeight); 
}


