import { pgTable, text, serial, integer, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export const hosts = pgTable("hosts", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  port: integer("port").notNull(),
  prefix: text("prefix").notNull(),
});

export const domains = pgTable("domains", {
  id: serial("id").primaryKey(),
  subdomain: text("subdomain").notNull().unique(),
  environment: text("environment").notNull(),
  hosts: jsonb("hosts").$type<Host[]>().notNull().default([]),
});

export const hostSchema = z.object({
  name: z.string().min(1, "Name is required"),
  port: z.number().min(1, "Port must be a positive number").max(65535, "Port must be less than 65536"),
  prefix: z.string().min(1, "Prefix is required"),
});

export const insertDomainSchema = createInsertSchema(domains, {
  subdomain: z.string().min(1, "Subdomain is required"),
  environment: z.enum(["production", "development", "staging", "testing"]),
  hosts: z.array(hostSchema).min(1, "At least one host is required"),
}).omit({ id: true });

export const updateDomainSchema = insertDomainSchema.partial();

export type Host = z.infer<typeof hostSchema>;
export type InsertDomain = z.infer<typeof insertDomainSchema>;
export type UpdateDomain = z.infer<typeof updateDomainSchema>;
export type Domain = typeof domains.$inferSelect;
