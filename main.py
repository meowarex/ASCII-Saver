#!/usr/bin/env python3

import sys
import os
import importlib
import pkgutil
import random
from typing import List, Generator
from pathlib import Path


class EffectLibrary:
    """Manages available visual effects and their selection"""
    
    def __init__(self):
        self.available_effects = self._discover_effects()
        self.effect_pool = self.available_effects.copy()
        random.shuffle(self.effect_pool)
        self.current_index = 0
    
    def _discover_effects(self) -> List[str]:
        """Dynamically discover available effects from the library. (in case of new effects in updates or whatever.)"""
        try:
            from terminaltexteffects import effects
            discovered = []
            
            # Scan all modules in effects package
            for importer, modname, ispkg in pkgutil.iter_modules(effects.__path__):
                if modname.startswith("effect_"):
                    effect_name = modname.replace("effect_", "").replace("_", " ").title()
                    discovered.append(effect_name)
            
            if discovered:
                print(f"Discovered {len(discovered)} effects", file=sys.stderr)
                return sorted(discovered)
            else:
                return self._fallback_effects()
        except Exception as e:
            print(f"Auto-discovery failed: {e}, using fallback list", file=sys.stderr)
            return self._fallback_effects()
    
    @staticmethod
    def _fallback_effects() -> List[str]:
        """Fallback list of known effects. (in case of auto-discovery failing and stuff)"""
        return [
            "Beams", "BinaryPath", "Blackhole", "BouncyBalls", "Bubbles",
            "Burn", "ColorShift", "Crumble", "Decrypt", "ErrorCorrect",
            "Expand", "Fireworks", "Highlight", "LaserEtch", "Matrix",
            "MiddleOut", "OrbittingVolley", "Overflow", "Pour", "Print",
            "Rain", "Random Sequence", "Rings", "Scattered", "Slice",
            "Slide", "Spotlights", "Spray", "Swarm", "Sweep", "SynthGrid",
            "Unstable", "VHSTape", "Waves", "Wipe",
        ]
    
    def get_next_effect(self) -> str:
        """Get the next effect in rotation, cycling through all effects"""
        if not self.effect_pool:
            self.effect_pool = self.available_effects.copy()
            random.shuffle(self.effect_pool)
        
        effect = self.effect_pool.pop(0)
        return effect
    
    def load_effect_class(self, effect_name: str):
        """Dynamically load and return an effect class"""
        module_name = "_".join(effect_name.lower().split())
        module_path = f"terminaltexteffects.effects.effect_{module_name}"
        
        try:
            module = importlib.import_module(module_path)
            class_name = "".join(effect_name.split())
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            return None


class DisplayContent:
    """Manages the content to be displayed"""
    
    def __init__(self, content_path: str = "content.txt"):
        self.content = self._load_content(content_path)
    
    def _load_content(self, path: str) -> str:
        """Load content from file or use default"""
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            return self._get_default_content()
    
    @staticmethod
    def _get_default_content() -> str:
        """Provide default content if file doesn't exist"""
        return """
   ▄▄▄▄███▄▄▄▄      ▄████████  ▄██████▄   ▄█     █▄     ▄████████    ▄████████    ▄████████ ▀████    ▐████▀ 
 ▄██▀▀▀███▀▀▀██▄   ███    ███ ███    ███ ███     ███   ███    ███   ███    ███   ███    ███   ███▌   ████▀  
 ███   ███   ███   ███    █▀  ███    ███ ███     ███   ███    ███   ███    ███   ███    █▀     ███  ▐███    
 ███   ███   ███  ▄███▄▄▄     ███    ███ ███     ███   ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄        ▀███▄███▀    
 ███   ███   ███ ▀▀███▀▀▀     ███    ███ ███     ███ ▀███████████ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀        ████▀██▄     
 ███   ███   ███   ███    █▄  ███    ███ ███     ███   ███    ███ ▀███████████   ███    █▄    ▐███  ▀███    
 ███   ███   ███   ███    ███ ███    ███ ███ ▄█▄ ███   ███    ███   ███    ███   ███    ███  ▄███     ███▄  
  ▀█   ███   █▀    ██████████  ▀██████▀   ▀███▀███▀    ███    █▀    ███    ███   ██████████ ████       ███▄ 
                                                                    ███    ███                              
        """
    
    def get(self) -> str:
        """Return the content to display"""
        return self.content


class Screensaver:
    """Main screensaver application orchestrator (big word i know)"""
    
    def __init__(self, content: str):
        self.content = content
        self.library = EffectLibrary()
        self.running = True
    
    def _configure_effect(self, effect_instance):
        """Apply standard configuration to any effect"""
        effect_instance.terminal_config.canvas_width = 0
        effect_instance.terminal_config.canvas_height = 0
        effect_instance.terminal_config.anchor_text = "c"
    
    def _render_effect(self, effect_class):
        """Render a single effect with error handling"""
        try:
            instance = effect_class(self.content)
            self._configure_effect(instance)
            
            with instance.terminal_output() as terminal:
                for frame in instance:
                    if not self.running:
                        return False
                    terminal.print(frame)
            return True
        except Exception as e:
            print(f"Error rendering effect: {e}", file=sys.stderr)
            return False
    
    def run(self):
        """Main loop - continuously cycle through effects"""
        try:
            while self.running:
                effect_name = self.library.get_next_effect()
                effect_class = self.library.load_effect_class(effect_name)
                
                if effect_class:
                    os.system("clear")
                    self._render_effect(effect_class)
        
        except KeyboardInterrupt:
            self.stop()
        finally:
            self.cleanup()
    
    def stop(self):
        """Signal the screensaver to stop"""
        self.running = False
    
    @staticmethod
    def cleanup():
        """Cleanup on exit"""
        os.system("clear")
        print("Screensaver stopped.", file=sys.stderr)


def main():
    """Entry point"""
    content_loader = DisplayContent()
    screensaver = Screensaver(content_loader.get())
    screensaver.run()


if __name__ == "__main__":
    main()
