export interface ApiEnvelope<T> {
  success: boolean;
  data: T;
  message: string | null;
  pagination?: Pagination;
}

export interface Pagination {
  page: number;
  size: number;
  totalElements: number;
  totalPages: number;
}

export interface User {
  id: number;
  fullName: string;
  email: string;
  roles: string[];
  status?: string;
  department?: string;
  position?: string;
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
  displayOrder: number;
  dashboardCount?: number;
}

export interface CategoryMini {
  id: number;
  name: string;
  slug: string;
}

export interface DashboardCard {
  id: number;
  title: string;
  slug: string;
  description: string;
  category: CategoryMini;
  tags: string[];
  accessLevel: string;
  status: string;
  sheetCount: number;
  lastUpdatedAt: string | null;
}

export interface Sheet {
  id: number;
  dashboardId: number;
  title: string;
  slug: string;
  description: string;
  displayOrder: number;
}

export interface FaqItem {
  question: string;
  answer: string;
}

export interface LearningMaterial {
  id: number;
  dashboardId: number;
  title: string;
  content: string;
  videoUrl: string;
  presentationUrl: string;
  faq: FaqItem[] | null;
}

export interface DashboardDetail extends DashboardCard {
  businessPurpose: string;
  ownerName: string;
  sheets: Sheet[];
  learningMaterial: LearningMaterial | null;
}

export interface Kpi {
  key: string;
  label: string;
  value: number;
  format: "currency" | "number";
}

export interface ChartPoint {
  label: string;
  value: number;
}

export interface ChartBlock {
  type: "BAR_CHART" | "LINE_CHART" | "PIE_CHART";
  title: string;
  data: ChartPoint[];
}

export interface TableColumn {
  key: string;
  label: string;
}

export interface DashboardData {
  filters: Record<string, string>;
  kpis: Kpi[];
  charts: ChartBlock[];
  table: { columns: TableColumn[]; rows: Record<string, any>[] };
}

export interface AuditLog {
  id: number;
  user: { id: number; fullName: string; email: string } | null;
  action: string;
  targetType: string;
  targetId: number | null;
  metadata: Record<string, any> | null;
  ipAddress: string;
  createdAt: string;
}
