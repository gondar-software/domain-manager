import { pgTable, text, serial, integer, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export enum HostType {
  DEFAULT = "default",
  WEBSOCKET = "websocket"
}

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
  type: z.nativeEnum(HostType).default(HostType.DEFAULT),
  host: z.string().url("Host must be a valid URL").min(1, "Host is required"),
  path: z.string().min(1, "Prefix is required"),
});

export const insertDomainSchema = createInsertSchema(domains, {
  subdomain: z.string().min(1, "Subdomain is required"),
  hosts: z.array(hostSchema).min(1, "At least one host is required"),
}).omit({ id: true });

export const updateDomainSchema = insertDomainSchema.partial();

export type InsertDomain = z.infer<typeof insertDomainSchema>;
export type UpdateDomain = z.infer<typeof updateDomainSchema>;

export interface Host {
  type: HostType;
  host: string;
  path: string;
}

export interface Domain {
  domain: string;
  hosts: Host[];
}