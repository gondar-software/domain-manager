import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Edit, Trash2 } from "lucide-react";
import { Domain } from "@/shared/schema";

interface DomainCardProps {
  domain: Domain;
  onEdit: (domain: Domain) => void;
  onDelete: (domain: Domain) => void;
}

export function DomainCard({ domain, onEdit, onDelete }: DomainCardProps) {
  const getEnvironmentColor = (environment: string) => {
    switch (environment) {
      case 'production':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'development':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'staging':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'testing':
        return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  const getHostTypeColor = (name: string) => {
    const lowerName = name.toLowerCase();
    if (lowerName.includes('frontend') || lowerName.includes('web')) {
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    } else if (lowerName.includes('backend') || lowerName.includes('api')) {
      return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
    } else if (lowerName.includes('database') || lowerName.includes('db')) {
      return 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200';
    } else {
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
    }
  };

  return (
    <Card>
      <CardContent className="p-6">
        <div className="flex justify-between items-start mb-4">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              {domain.subdomain}
            </h3>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {domain.environment.charAt(0).toUpperCase() + domain.environment.slice(1)} environment
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge className={getEnvironmentColor(domain.environment)}>
              {domain.environment}
            </Badge>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onEdit(domain)}
              className="h-8 w-8 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              <Edit className="h-4 w-4" />
            </Button>
            <Button
              variant="ghost"
              size="icon"
              onClick={() => onDelete(domain)}
              className="h-8 w-8 text-red-500 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {domain.hosts.map((host, index) => (
            <div key={index} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-900 dark:text-white">
                  {host.name}
                </span>
                <Badge className={getHostTypeColor(host.name)} variant="secondary">
                  {host.name.toLowerCase().includes('frontend') || host.name.toLowerCase().includes('web') ? 'WEB' :
                   host.name.toLowerCase().includes('backend') || host.name.toLowerCase().includes('api') ? 'API' :
                   host.name.toLowerCase().includes('database') || host.name.toLowerCase().includes('db') ? 'DB' : 'SVC'}
                </Badge>
              </div>
              <div className="space-y-1 text-sm text-gray-600 dark:text-gray-400">
                <div className="flex justify-between">
                  <span>Port:</span>
                  <span>{host.port}</span>
                </div>
                <div className="flex justify-between">
                  <span>Prefix:</span>
                  <span>{host.prefix}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
