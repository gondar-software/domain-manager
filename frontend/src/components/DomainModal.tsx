import { useEffect, useState } from "react";
import { useForm, useFieldArray } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Plus, Trash2 } from "lucide-react";
import { insertDomainSchema, Domain, type InsertDomain, HostType } from "@/shared/schema";

interface DomainModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (data: InsertDomain) => void;
  domain?: Domain;
  isLoading?: boolean;
}

export function DomainModal({ isOpen, onClose, onSubmit, domain, isLoading }: DomainModalProps) {
  const [isEditing, setIsEditing] = useState(false);

  const form = useForm<InsertDomain>({
    resolver: zodResolver(insertDomainSchema),
    defaultValues: {
      domain: "",
      hosts: [{ type: HostType.DEFAULT, host: "http://localhost:3000", path: "/" }],
    },
  });

  const { fields, append, remove } = useFieldArray({
    control: form.control,
    name: "hosts",
  });

  useEffect(() => {
    if (domain) {
      setIsEditing(true);
      form.reset({
        domain: domain.domain,
        hosts: domain.hosts,
      });
    } else {
      setIsEditing(false);
      form.reset({
        domain: "",
        hosts: [{ type: HostType.DEFAULT, host: "http://localhost:3000", path: "/" }],
      });
    }
  }, [domain, form]);

  const handleSubmit = (data: InsertDomain) => {
    onSubmit(data);
  };

  const addHost = () => {
    append({ type: HostType.DEFAULT, host: "http://localhost:3000", path: "/" });
  };

  const removeHost = (index: number) => {
    if (fields.length > 1) {
      remove(index);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="max-w-4xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? "Edit Domain Configuration" : "Add Domain Configuration"}
          </DialogTitle>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
            <div className="space-y-4">
              <h3 className="text-lg font-medium">Domain Information</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="domain"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Domain</FormLabel>
                      <FormControl>
                        <Input placeholder="api.example.com" {...field} />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-medium">Host Configurations</h3>
                <Button type="button" onClick={addHost} variant="outline" size="sm">
                  <Plus className="h-4 w-4 mr-2" />
                  Add Host
                </Button>
              </div>

              <div className="space-y-4">
                {fields.map((field, index) => (
                  <div key={field.id} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                    <div className="flex justify-between items-center mb-4">
                      <h4 className="text-sm font-medium">Host #{index + 1}</h4>
                      <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        onClick={() => removeHost(index)}
                        disabled={fields.length === 1}
                        className="text-red-500 hover:text-red-700"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <FormField
                        control={form.control}
                        name={`hosts.${index}.type`}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Type</FormLabel>
                            <Select onValueChange={field.onChange} defaultValue={field.value}>
                              <FormControl>
                                <SelectTrigger>
                                  <SelectValue placeholder="Select host type" />
                                </SelectTrigger>
                              </FormControl>
                              <SelectContent>
                                {Object.values(HostType).map((type) => (
                                  <SelectItem key={type} value={type}>
                                    {type === HostType.DEFAULT ? "Default Host" : "WebSocket Host"}
                                  </SelectItem>
                                ))}
                              </SelectContent>
                            </Select>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name={`hosts.${index}.host`}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Host</FormLabel>
                            <FormControl>
                              <Input
                                type="url"
                                placeholder="http://localhost:3000"
                                {...field}
                              />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />

                      <FormField
                        control={form.control}
                        name={`hosts.${index}.path`}
                        render={({ field }) => (
                          <FormItem>
                            <FormLabel>Prefix</FormLabel>
                            <FormControl>
                              <Input placeholder="/" {...field} />
                            </FormControl>
                            <FormMessage />
                          </FormItem>
                        )}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="flex justify-end space-x-4 pt-4 border-t">
              <Button type="button" variant="outline" onClick={onClose}>
                Cancel
              </Button>
              <Button type="submit" disabled={isLoading}>
                {isLoading ? "Saving..." : "Save Domain"}
              </Button>
            </div>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  );
}