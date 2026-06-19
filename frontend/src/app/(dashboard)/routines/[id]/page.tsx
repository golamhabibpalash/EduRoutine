import { RoutineDetailPage } from "@/features/routines/pages/RoutineDetailPage"

interface Props {
  params: Promise<{ id: string }>
}

export default async function RoutineDetailRoute({ params }: Props) {
  const { id } = await params
  return <RoutineDetailPage routineId={id} />
}
