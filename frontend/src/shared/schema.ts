import { pgTable, text, jsonb } from "drizzle-orm/pg-core";
import { createInsertSchema } from "drizzle-zod";
import { z } from "zod";

export enum HostType {
  DEFAULT = "default",
  WEBSOCKET = "websocket"
}

export const domains = pgTable("domains", {
  domain: text("subdomain").notNull().unique(),
  hosts: jsonb("hosts").$type<Host[]>().notNull().default([]),
});

export const hostSchema = z.object({
  type: z.nativeEnum(HostType).default(HostType.DEFAULT),
  host: z.string().url("Host must be a valid URL").min(1, "Host is required"),
  path: z.string().min(1, "Prefix is required"),
});

export const insertDomainSchema = createInsertSchema(domains, {
  domain: z.string().min(1, "Domain is required"),
  hosts: z.array(hostSchema).min(1, "At least one host is required"),
});

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