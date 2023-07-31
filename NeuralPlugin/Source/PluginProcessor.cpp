#include "PluginProcessor.h"
#include "PluginEditor.h"
#include <fstream>
#include <iostream>
#include <filesystem>
//==============================================================================

NeuralPluginAudioProcessor::NeuralPluginAudioProcessor() :
#if JUCE_IOS || JUCE_MAC
    AudioProcessor(juce::JUCEApplicationBase::isStandaloneApp() ?
        BusesProperties().withInput("Input", juce::AudioChannelSet::mono(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true) :
        BusesProperties().withInput("Input", juce::AudioChannelSet::stereo(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true)),
#else
    AudioProcessor(BusesProperties().withInput("Input", juce::AudioChannelSet::stereo(), true)
        .withOutput("Output", juce::AudioChannelSet::stereo(), true)),
#endif
    parameters(*this, nullptr, Identifier("Parameters"),
        {
            std::make_unique<AudioParameterFloat>("gain_db", "Gain [dB]", -12.0f, 12.0f, 0.0f),
            std::make_unique<AudioParameterChoice>("model_type", "Model Type", StringArray { "Run-Time", "Compile-Time" }, 0)
        })
{
    inGainDbParam = parameters.getRawParameterValue("gain_db");
    modelTypeParam = parameters.getRawParameterValue("model_type");

    auto modelFilePath = "C:/Users/Utente/OneDrive - Politecnico di Milano/Immagini/Documenti/Development/Python/PROJECT-STMAE/neural3.json";
    assert(std::filesystem::exists(modelFilePath));

    std::ifstream jsonStream(modelFilePath, std::ifstream::binary);
    nlohmann::json jsonInput;
    jsonStream >> jsonInput;
    models[0] = RTNeural::json_parser::parseJson<float>(jsonInput);
    std::ifstream jsonStream1(modelFilePath, std::ifstream::binary);
    nlohmann::json jsonInput1;
    jsonStream1 >> jsonInput1;
    models[1] = RTNeural::json_parser::parseJson<float>(jsonInput1);

}

NeuralPluginAudioProcessor::~NeuralPluginAudioProcessor()
{
}

//==============================================================================
const String NeuralPluginAudioProcessor::getName() const
{
    return JucePlugin_Name;
}

bool NeuralPluginAudioProcessor::acceptsMidi() const
{
#if JucePlugin_WantsMidiInput
    return true;
#else
    return false;
#endif
}

bool NeuralPluginAudioProcessor::producesMidi() const
{
#if JucePlugin_ProducesMidiOutput
    return true;
#else
    return false;
#endif
}

bool NeuralPluginAudioProcessor::isMidiEffect() const
{
#if JucePlugin_IsMidiEffect
    return true;
#else
    return false;
#endif
}

double NeuralPluginAudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int NeuralPluginAudioProcessor::getNumPrograms()
{
    return 1;   // NB: some hosts don't cope very well if you tell them there are 0 programs,
    // so this should be at least 1, even if you're not really implementing programs.
}

int NeuralPluginAudioProcessor::getCurrentProgram()
{
    return 0;
}

void NeuralPluginAudioProcessor::setCurrentProgram(int index)
{
}

const String NeuralPluginAudioProcessor::getProgramName(int index)
{
    return {};
}

void NeuralPluginAudioProcessor::changeProgramName(int index, const String& newName)
{
}

//==============================================================================
void NeuralPluginAudioProcessor::prepareToPlay(double sampleRate, int samplesPerBlock)
{
    *dcBlocker.state = *dsp::IIR::Coefficients<float>::makeHighPass(sampleRate, 35.0f);

    dsp::ProcessSpec spec{ sampleRate, static_cast<uint32> (samplesPerBlock), 2 };
    inputGain.prepare(spec);
    inputGain.setRampDurationSeconds(0.05);
    dcBlocker.prepare(spec);
    models[0]->reset();
    models[1]->reset();
}

void NeuralPluginAudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
}

bool NeuralPluginAudioProcessor::isBusesLayoutSupported(const BusesLayout& layouts) const
{
    // This is the place where you check if the layout is supported.
    // In this template code we only support mono or stereo.
    if (layouts.getMainOutputChannelSet() != AudioChannelSet::mono()
        && layouts.getMainOutputChannelSet() != AudioChannelSet::stereo())
        return false;

    // This checks if the input layout matches the output layout
    if (layouts.getMainOutputChannelSet() != layouts.getMainInputChannelSet())
        return false;

    return true;
}

void NeuralPluginAudioProcessor::processBlock(AudioBuffer<float>& buffer, MidiBuffer& midiMessages)
{
    dsp::AudioBlock<float> block(buffer);
    dsp::ProcessContextReplacing<float> context(block);

    //inputGain.setGainDecibels(inGainDbParam->load() + 25.0f);
    //inputGain.process(context);
    juce::ScopedNoDenormals noDenormals;
    auto totalNumInputChannels = getTotalNumInputChannels();
    auto totalNumOutputChannels = getTotalNumOutputChannels();
    for (auto i = totalNumInputChannels; i < totalNumOutputChannels; ++i)
        buffer.clear(i, 0, buffer.getNumSamples());


    // use compile-time model

    for (int ch = 0; ch < buffer.getNumChannels(); ++ch)
    {
        auto* x = buffer.getWritePointer(ch);
        for (int n = 0; n < buffer.getNumSamples(); ++n)
        {
            float input[] = {x[n],knob_value1,knob_value2,knob_value3};

            x[n] =( models[ch]->forward(input));

            DBG(x[n]);
        }
    }

    dcBlocker.process(context);
    buffer.applyGain(5.0f);

    ignoreUnused(midiMessages);
}

//==============================================================================
bool NeuralPluginAudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

juce::AudioProcessorEditor* NeuralPluginAudioProcessor::createEditor()
{
    return new NeuralPluginAudioProcessorEditor(*this);
}

//==============================================================================
void NeuralPluginAudioProcessor::getStateInformation(MemoryBlock& destData)
{

}

void NeuralPluginAudioProcessor::setStateInformation(const void* data, int sizeInBytes)
{

}

void NeuralPluginAudioProcessor::setValueKnob1(float knob_value)
{
    knob_value1 = knob_value;
}

void NeuralPluginAudioProcessor::setValueKnob2(float knob_value)
{
    knob_value2 = knob_value;
}

void NeuralPluginAudioProcessor::setValueKnob3(float knob_value)
{
    knob_value3 = knob_value;
}


//==============================================================================
// This creates new instances of the plugin..
AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new NeuralPluginAudioProcessor();
}
