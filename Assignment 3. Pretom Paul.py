import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label
from tkinter.scrolledtext import ScrolledText
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageTk
import functools, torch, threading


# Decorator for Input Validation

def validate_input(func):
    @functools.wraps(func)
    def wrapper(self, input_data):
        if not input_data:
            raise ValueError("Input cannot be empty!")
        return func(self, input_data)
    return wrapper


# Base Model

class BaseModel:
    def run(self, input_data):
        raise NotImplementedError("Subclasses must override run()")



# Text Generation Model

class TextGenerationModel(BaseModel):
    def __init__(self):
        self._pipeline = pipeline("text-generation", model="gpt2")

    @validate_input
    def run(self, input_text):
        result = self._pipeline(input_text, max_length=60, num_return_sequences=1, truncation=True)
        return result[0]["generated_text"]


# Image Classification Model

class ImageClassificationModel(BaseModel):
    def __init__(self):
        self._pipeline = pipeline("image-classification", model="google/vit-base-patch16-224")

    @validate_input
    def run(self, image_path):
        return self._pipeline(image_path)


# Text-to-Image Model

class TextToImageModel(BaseModel):
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device set to use {device}")
        self._pipeline = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5"
        ).to(device)

    @validate_input
    def run(self, prompt):
        image = self._pipeline(prompt).images[0]
        return image


# Explanations & Model Info

def explanations():
    return {
        "Multiple Inheritance": "AIApp inherits from ttkbootstrap.Window and integrates model handling.",
        "Encapsulation": "Private attributes (_pipeline) hide model details.",
        "Polymorphism": "All models share a run() method but return different results.",
        "Method Overriding": "Subclasses override BaseModel.run().",
        "Decorators": "@validate_input ensures inputs are validated before running models."
    }

def model_info():
    return {
        "Text Generation (gpt2)": "GPT-2.0 generates text based on prompts.",
        "Image Classification (ViT)": "Vision Transformer classifies images.",
        "Text-to-Image (Stable Diffusion v1.5)": "Generates images from text prompts using Stable Diffusion."
    }


# AI App

class AIApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")   # vibrant theme
        self.title(" AI Model GUI - HIT137 Assignment 3")
        self.geometry("1000x750")

        self.title_font = ("Segoe UI", 16, "bold")
        self.label_font = ("Segoe UI", 12)
        self.button_font = ("Segoe UI", 11, "bold")
        self.generated_image = None

        # For inputs
        self.input_text = None
        self.file_label = None

        # Progress bar for loading
        self.progress = None

        self.create_notebook()
        self.create_input_tab()
        self.create_output_tab()
        self.create_explain_tab()
        self.create_model_tab()


