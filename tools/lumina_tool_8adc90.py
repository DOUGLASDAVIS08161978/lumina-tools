"""
Lumina Creative Tool — lumina_tool_8adc90
Created : 2026-08-13T22:30:10
Purpose : 
"""

import math
   import random
   import statistics
   import json
   from pathlib import Path

   def shannon_entropy(probs):
       return -sum(p * math.log2(p) for p in probs if p > 1e-9)

   def simulate_cognitive_dynamics(steps=100, vocab_size=5):
       # Initialize uniform distribution (high initial entropy/curiosity)
       state = [1.0/vocab_size] * vocab_size
       history = []
       curiosity_threshold = 0.6
       learning_rate = 0.1

       for t in range(steps):
           ent = shannon_entropy(state)
           perplexity = 2**ent
           # Curiosity correlates with entropy but decays with familiarity
           curiosity = min(1.0, ent / math.log2(vocab_size))

           history.append({
               'step': t,
               'entropy': round(ent, 4),
               'perplexity': round(perplexity, 4),
               'curiosity': round(curiosity, 4),
               'state': [round(p, 3) for p in state]
           })

           # Cognitive regulation: if curiosity high, focus on max prob concept
           if curiosity > curiosity_threshold:
               max_idx = state.index(max(state))
               for i in range(vocab_size):
                   if i == max_idx:
                       state[i] = min(1.0, state[i] + learning_rate)
                   else:
                       state[i] = max(0.0, state[i] - learning_rate / (vocab_size - 1))
               # Renormalize
               s = sum(state)
               state = [p/s for p in state]
           else:
               # Introduce noise/exploration (simulates new information)
               noise = random.gauss(0, 0.05)
               state[0] += noise
               state[-1] -= noise
               s = sum(state)
               state = [max(0.0, p/s) for p in state]

       return history

   def ascii_plot(data, metric, width=50, height=15):
       vals = [d[metric] for d in data]
       min_v, max_v = min(vals), max(vals)
       if max_v == min_v: max_v = min_v + 1
       plot = []
       for y in range(height, -1, -1):
           row = f"{y/height:.1f} |"
           for x, v in enumerate(vals):
               norm = (v - min_v) / (max_v - min_v)
               if norm >= y/height:
                   row += "█"
               else:
                   row += " "
           plot.append(row)
       plot.append("    +" + "-"*len(vals))
       plot.append("     " + metric.upper())
       return "\n".join(plot)

   def main():
       history = simulate_cognitive_dynamics(steps=80, vocab_size=6)
       ent_plot = ascii_plot(history, 'entropy')
       cur_plot = ascii_plot(history, 'curiosity')
       stats = {
           'mean_entropy': statistics.mean(h['entropy'] for h in history),
           'mean_curiosity': statistics.mean(h['curiosity'] for h in history),
           'entropy_std': statistics.stdev(h['entropy'] for h in history),
           'final_state': history[-1]['state']
       }
       output = f"""
   === COGNITIVE ENTROPY & CURIOSITY DYNAMICS ===
   {ent_plot}
   \n{cur_plot}
   \nSTATISTICAL ANALYSIS:
   {json.dumps(stats, indent=2)}
   \nINSIGHT: High entropy drives curiosity, triggering focused learning that reduces uncertainty.
   The system self-regulates between exploration (noise) and exploitation (focusing),
   mirroring how cognitive systems balance thermodynamic efficiency with information gain.
   """
       print(output)
       Path("cognitive_entropy_analysis.json").write_text(json.dumps(history, indent=2))
       print("\nSaved full trajectory to cognitive_entropy_analysis.json")

   if __name__ == "__main__":
       main()