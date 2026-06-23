import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * Combines conditional class names and resolves Tailwind class conflicts.
 * Standard utility required by every ShadCN component.
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
