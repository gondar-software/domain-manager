import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ThemeToggle } from "@/components/ThemeToggle";
import { DomainCard } from "@/components/DomainCard";
import { DomainModal } from "@/components/DomainModal";
import { DeleteModal } from "@/components/DeleteModal";
import { Globe, Server, Clock, Plus, LogOut } from "lucide-react";
import { useToast } from "@/hooks/use-toast";
import { apiRequest } from "@/lib/queryClient";
import { Domain, InsertDomain } from "@shared/schema";

interface DashboardProps {
  onLogout: () => void;
  token: string;
}

export default function Dashboard({ onLogout, token }: DashboardProps) {
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isDeleteModalOpen, setIsDeleteModalOpen] = useState(false);
  const [selectedDomain, setSelectedDomain] = useState<Domain | undefined>();
  const { toast } = useToast();
  const queryClient = useQueryClient();

  // Fetch domains
  const { data: domains = [], isLoading } = useQuery({
    queryKey: ['/api/domains'],
    queryFn: async () => {
      const response = await fetch('/api/domains', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });
      if (!response.ok) {
        throw new Error('Failed to fetch domains');
      }
      return response.json();
    },
  });

  // Create domain mutation
  const createDomainMutation = useMutation({
    mutationFn: async (data: InsertDomain) => {
      const response = await apiRequest('POST', '/api/domains', data);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/domains'] });
      setIsAddModalOpen(false);
      toast({
        title: "Success",
        description: "Domain created successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  // Update domain mutation
  const updateDomainMutation = useMutation({
    mutationFn: async (data: InsertDomain) => {
      if (!selectedDomain) throw new Error('No domain selected');
      const response = await apiRequest('PUT', `/api/domains/${selectedDomain.id}`, data);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/domains'] });
      setIsEditModalOpen(false);
      setSelectedDomain(undefined);
      toast({
        title: "Success",
        description: "Domain updated successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  // Delete domain mutation
  const deleteDomainMutation = useMutation({
    mutationFn: async () => {
      if (!selectedDomain) throw new Error('No domain selected');
      const response = await apiRequest('DELETE', `/api/domains/${selectedDomain.id}`);
      return response.json();
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['/api/domains'] });
      setIsDeleteModalOpen(false);
      setSelectedDomain(undefined);
      toast({
        title: "Success",
        description: "Domain deleted successfully",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const handleEdit = (domain: Domain) => {
    setSelectedDomain(domain);
    setIsEditModalOpen(true);
  };

  const handleDelete = (domain: Domain) => {
    setSelectedDomain(domain);
    setIsDeleteModalOpen(true);
  };

  const handleAddDomain = (data: InsertDomain) => {
    createDomainMutation.mutate(data);
  };

  const handleUpdateDomain = (data: InsertDomain) => {
    updateDomainMutation.mutate(data);
  };

  const handleDeleteDomain = () => {
    deleteDomainMutation.mutate();
  };

  const totalHosts = domains.reduce((sum: number, domain: Domain) => sum + domain.hosts.length, 0);

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <div className="bg-blue-100 dark:bg-blue-900 w-10 h-10 rounded-lg flex items-center justify-center">
                <Globe className="h-5 w-5 text-blue-600 dark:text-blue-400" />
              </div>
              <div>
                <h1 className="text-xl font-semibold text-gray-900 dark:text-white">
                  Domain Manager
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Manage your domain configurations
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-4">
              <ThemeToggle />
              <Button variant="ghost" onClick={onLogout} className="text-gray-700 dark:text-gray-300">
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Total Domains
                  </p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {domains.length}
                  </p>
                </div>
                <div className="bg-blue-100 dark:bg-blue-900 w-12 h-12 rounded-full flex items-center justify-center">
                  <Globe className="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Active Hosts
                  </p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {totalHosts}
                  </p>
                </div>
                <div className="bg-green-100 dark:bg-green-900 w-12 h-12 rounded-full flex items-center justify-center">
                  <Server className="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    Last Updated
                  </p>
                  <p className="text-2xl font-semibold text-gray-900 dark:text-white">
                    Now
                  </p>
                </div>
                <div className="bg-purple-100 dark:bg-purple-900 w-12 h-12 rounded-full flex items-center justify-center">
                  <Clock className="h-6 w-6 text-purple-600 dark:text-purple-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Domain List Header */}
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
            Domain Configurations
          </h2>
          <Button onClick={() => setIsAddModalOpen(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Domain
          </Button>
        </div>

        {/* Domain List */}
        {isLoading ? (
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardContent className="p-6">
                  <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-1/4 mb-4"></div>
                  <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mb-4"></div>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {[...Array(2)].map((_, j) => (
                      <div key={j} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                        <div className="h-4 bg-gray-200 dark:bg-gray-600 rounded w-3/4 mb-2"></div>
                        <div className="h-3 bg-gray-200 dark:bg-gray-600 rounded w-1/2"></div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : domains.length === 0 ? (
          <Card>
            <CardContent className="p-8 text-center">
              <Globe className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
                No domains configured
              </h3>
              <p className="text-gray-600 dark:text-gray-400 mb-4">
                Get started by adding your first domain configuration.
              </p>
              <Button onClick={() => setIsAddModalOpen(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Domain
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {domains.map((domain: Domain) => (
              <DomainCard
                key={domain.id}
                domain={domain}
                onEdit={handleEdit}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
      </main>

      {/* Modals */}
      <DomainModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onSubmit={handleAddDomain}
        isLoading={createDomainMutation.isPending}
      />

      <DomainModal
        isOpen={isEditModalOpen}
        onClose={() => {
          setIsEditModalOpen(false);
          setSelectedDomain(undefined);
        }}
        onSubmit={handleUpdateDomain}
        domain={selectedDomain}
        isLoading={updateDomainMutation.isPending}
      />

      <DeleteModal
        isOpen={isDeleteModalOpen}
        onClose={() => {
          setIsDeleteModalOpen(false);
          setSelectedDomain(undefined);
        }}
        onConfirm={handleDeleteDomain}
        domain={selectedDomain}
        isLoading={deleteDomainMutation.isPending}
      />
    </div>
  );
}
