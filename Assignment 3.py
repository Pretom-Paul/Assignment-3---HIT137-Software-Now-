import ttkbootstrap as tb
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, Label
from tkinter.scrolledtext import ScrolledText
from transformers import pipeline
from diffusers import StableDiffusionPipeline
from PIL import Image, ImageTk
import functools, torch, threading
