import { z } from 'zod';

/**
 * Authentication Form Schemas
 */

export const RegisterSchema = z.object({
  email: z.string()
    .email('Invalid email format')
    .min(3, 'Email must be at least 3 characters'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[0-9]/, 'Password must contain at least one digit')
    .regex(/[a-zA-Z]/, 'Password must contain at least one letter'),
  passwordConfirm: z.string(),
  name: z.string()
    .min(1, 'Name is required')
    .max(100, 'Name must be less than 100 characters')
}).refine((data: { password: string; passwordConfirm: string }) => data.password === data.passwordConfirm, {
  message: 'Passwords must match',
  path: ['passwordConfirm']
});

export type RegisterInput = z.infer<typeof RegisterSchema>;

export const LoginSchema = z.object({
  email: z.string()
    .email('Invalid email format'),
  password: z.string()
    .min(1, 'Password is required')
});

export type LoginInput = z.infer<typeof LoginSchema>;

/**
 * Session Form Schemas
 */

export const SessionCreateSchema = z.object({
  practice_type: z.enum(['chords', 'scales', 'course', 'songs']),
  tempo: z.number().int().min(90).max(120).optional().nullable(),
  notes: z.string().max(500, 'Notes must be less than 500 characters').optional().nullable()
}).refine(
  (data) => {
    // Tempo required for chords and scales
    if (['chords', 'scales'].includes(data.practice_type)) {
      return data.tempo !== undefined && data.tempo !== null;
    }
    // Tempo not allowed for course and songs
    if (['course', 'songs'].includes(data.practice_type)) {
      return data.tempo === undefined || data.tempo === null;
    }
    return true;
  },
  {
    message: 'Tempo validation failed',
    path: ['tempo']
  }
);

export type SessionCreateInput = z.infer<typeof SessionCreateSchema>;

export const SessionUpdateSchema = z.object({
  notes: z.string().max(500, 'Notes must be less than 500 characters').optional().nullable()
});

export type SessionUpdateInput = z.infer<typeof SessionUpdateSchema>;

/**
 * Validation Error Handler
 */

export interface ValidationResult<T> {
  success: boolean;
  data?: T;
  errors?: Record<string, string>;
}

export function validateForm<T>(schema: z.ZodSchema, data: unknown): ValidationResult<T> {
  const result = schema.safeParse(data);
  if (result.success) {
    return { success: true, data: result.data as T };
  }

  const errors: Record<string, string> = {};
  result.error.errors.forEach((err: z.ZodError['errors'][0]) => {
    const path = err.path.join('.');
    errors[path] = err.message;
  });

  return { success: false, errors };
}

/**
 * Helper function to get field error
 */
export function getFieldError(errors: Record<string, string> | undefined, field: string): string | undefined {
  return errors?.[field];
}
